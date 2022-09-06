import os
print("Warning:Installing tesseract on machine")
os.system('apt-get install tesseract-ocr -y')
print("tesseract should be installed")

import time
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification, LayoutLMv3FeatureExtractor
from datasets import load_dataset
from PIL import Image, ImageDraw, ImageFont
import argparse

dataset = load_dataset("nielsr/funsd", split="test")

# define id2label, label2color
labels = dataset.features['ner_tags'].feature.names
id2label = {v: k for v, k in enumerate(labels)}
label2color = {'question':'blue', 'answer':'green', 'header':'orange', 'other':'violet'}
l2l = {'question':'key', 'answer':'value', 'header':'title'}
f_labels = {'question':'key', 'answer':'value', 'header':'title', 'other':'others'}


processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = LayoutLMv3ForTokenClassification.from_pretrained("nielsr/layoutlmv3-finetuned-funsd",ignore_mismatched_sizes = True)
feature_extractor = LayoutLMv3FeatureExtractor()

def iob_to_label(label):
    label = label[2:]
    if not label:
      return 'other'
    return label

def unnormalize_box(bbox, width, height):
     return [
         width * (bbox[0] / 1000),
         height * (bbox[1] / 1000),
         width * (bbox[2] / 1000),
         height * (bbox[3] / 1000),
     ]

import json
def normalize_box(box, width, height):
    return [
        int(1000 * (box[0] / width)),
        int(1000 * (box[1] / height)),
        int(1000 * (box[2] / width)),
        int(1000 * (box[3] / height)),
    ]

def parsing(true_predictions,token_boxes,bbdict):  
  cluster_master=[]
  cluster=[]
  tbox_list = []
  picked=[]
  prev=''

  for prediction,tbox in zip(true_predictions,token_boxes):
#     print(prediction,tbox)
    x,y=tbox[:2]
    if tbox not in picked:
      picked.append(tbox)
    else:
      continue
    try:

      word=bbdict[str(tbox)]
      gap=False
      if x-prevx > 150 or y-prevy > 20 :
        gap=True

      if prediction in ['B-QUESTION','I-QUESTION']:
        if prev=='value':
          cluster_master.append((cluster,'value',x,y,tbox_list))
          cluster=[]
          tbox_list = []
        elif gap:
          cluster_master.append((cluster,prev,x,y,tbox_list))
          cluster=[]
          tbox_list = []

        cluster.append(word)
        tbox_list.append(tbox)
        prev='key'
      else:
        if prev=='key' :
          cluster_master.append((cluster,'key',x,y,tbox_list))
          cluster=[]
          tbox_list = []
        elif gap:
          cluster_master.append((cluster,prev,x,y,tbox_list))
          cluster=[]
          tbox_list = []
        cluster.append(word)
        tbox_list.append(tbox)
        prev='value'
      
      
    except:
      pass
    prevx=x
    prevy=y
    
  cluster_master.append((cluster,prev,x,y,tbox_list))
  # return cluster_master


  key_value=dict()
  for item in cluster_master:
#     print('item',item)
    typ=item[1]
    text=' '.join(item[0])
    x,y=item[2:4]
    
    if typ=='value' and prevtyp=='key':
      key_value[prevtext]=text


    prevtext=text
    prevtyp=typ
    prevx=x
    prevy=y

  return key_value,cluster_master

def con_coordinates(lst):
    try:
        x1 = lst[0][0]
        y1 = lst[0][1]
        x2 = lst[0][2]
        y2 = lst[0][3]
        for i in range(1,len(lst)):
            if lst[i][0] < x1:
                x1 = lst[i][0]
            if lst[i][1] < y1:
                y1 = lst[i][1]
            if lst[i][2] > x2:
                x2 = lst[i][2]
            if lst[i][3] > y2:
                y2 = lst[i][3]
        return [x1,y1,x2,y2]
    except Exception as e:
        return []
            



def main(img):
    
  image = img.convert("RGB")
  
  width, height = image.size
  features = feature_extractor(image, return_tensors="pt")
  words,boxes=features['words'][0],features['boxes'][0]

  bbdict=dict()
  for word,box in zip(words,boxes):
    bbdict[str(box)]=word
  start=time.time()
  encoding = processor(image, words, boxes=boxes, return_tensors="pt")
  outputs = model(**encoding)
  print('Results Exported Sucessfully at results/final_annotated')


  # get predictions
  predictions = outputs.logits.argmax(-1).squeeze().tolist()
  token_boxes = encoding.bbox.squeeze().tolist()
  true_predictions = [id2label[pred] for idx, pred in enumerate(predictions)]
  true_boxes = [unnormalize_box(box, width, height) for idx, box in enumerate(token_boxes)]

    # draw predictions over the image
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("tools/arial/arial.ttf", 10, encoding="unic")
  for prediction, box in zip(true_predictions, true_boxes):
      predicted_label = iob_to_label(prediction).lower()
      if predicted_label != 'other' and predicted_label !='header' :
          draw.rectangle(box, outline=label2color[predicted_label])
          draw.text((box[0]+10, box[1]-10), f_labels[predicted_label], fill=label2color[predicted_label])
      else:
        continue
  output,cluster_master=parsing(true_predictions,token_boxes,bbdict)
 ## saving output key value dict as json file
  json_name = str(im.filename.split('/')[-1].split('.')[0])+'_key_value'+'.json'
  with open(os.path.join('results/json_output/',json_name), 'w') as fp:
    json.dump(output, fp)
## saving funsd annnotated image
  
  filename = str(im.filename.split('/')[-1].split('.')[0])+'_annotated'+'.jpeg'
  image.save(os.path.join('results/funsd_output',filename))

  key_boxes = []
  for item in cluster_master:
    key_boxes.append((item[0], item[1], item[2], item[3], con_coordinates(item[4])))
    

  key_box=dict()
  for item in key_boxes:
    typ=item[1]
    text=' '.join(item[0])
    x,y=item[2:4]

    if typ=='value' and prevtyp=='key':
      key_box[prevtext]={'value':text,'box':item[4]}

    prevtext=text
    prevtyp=typ
    prevx=x
    prevy=y
  draw = ImageDraw.Draw(img)
  for item in key_box.items():
    box = unnormalize_box(item[1]['box'],width,height)
    draw.rectangle(box, outline='green')
    draw.text((box[0]+10, box[1]-10), item[0], outline='green', font=font)
    filename =  str(im.filename.split('/')[-1].split('.')[0])+'_annotated'+'.jpg'
    ## saving post processed annnotated image

    im.save((os.path.join('results/final_annotated',filename)))

         
  return img,output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, required=True, help='Input Image')
    args = parser.parse_args()
    im = Image.open(args.i)
    main(im)

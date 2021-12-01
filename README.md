# Product-Count-Violation

# ML Model detection data:
1. Pins and core detection ( presented in the moulding machine from Loading to shifting).
2. Draw Region (Identifies Loading region and shifting  or transport region).
3. Product counting violation detection (between time of entering and to shifting from transport region). 
  
  Core Violation: The actual no.of the cores  aren’t presented in the mold. 

## Annotation:
  Images extracted from the video then annotate by using the Labelimg tool
  
## Custom Object Detection:
  yolov3-tiny model is used to detect the objects
  

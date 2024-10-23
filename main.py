import threading
import sqlite3
import requests
import zxingcpp
import cv2
from helper import (
    cam1, 
    cam2, 
    fetch_names_with_status_false,
    update_status_to_true

)



def decode_everything():
    while True:
        images = fetch_names_with_status_false()
        
        for image in images :
            img = cv2.imread(str(image),0)
            if img is not None:
                img_height, img_width = img.shape
                crop_width, crop_height = (512,512)
                step=100
                a=[]
                _results=[]
                for y in range(0, img_height - crop_height + 1, step):
                    for x in range(0, img_width - crop_width + 1, step):
                        # Extract the crop from the image
                        crop = img[y:y + crop_height, x:x + crop_width]
                        try:
                            results = zxingcpp.read_barcodes(crop)

                            for result in results:
                                if result.text not in a:
                                    a.append(result.text)
                                    obj ={
                                    "value":result.text,
                                        "type":result.format.name
                                    }
                                    #print(obj)
                                    _results.append(obj)
                        except Exception:
                            pass
                
                data={"total_detection":len(_results), "data":_results, "imagename":image[4:-4]}
                
                requests.patch("https://comfortwall.firebaseio.com/step1.json", json=data)
                update_status_to_true(image)
               # os.system(f'curl -F "file=@{image}" http://160.238.95.111/upload')

thread1 = threading.Thread(target=cam1)
thread2 = threading.Thread(target=cam2)
thread3 = threading.Thread(target=decode_everything)

# Start the threads
thread1.start()
thread2.start()
thread3.start()


# Keep the main thread running to allow the other threads to continue execution
thread1.join()
thread2.join()
thread3.join()
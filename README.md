# Picture-Transfer

This repo provides PyTorch Implementation of **[MSG-Net](#msg-net)** and **[Neural Style](#neural-style)**.

### Stylize Images Using Pre-trained MSG-Net
0. Download the pre-trained model
	```bash
	git clone git@github.com:xmg2024/Picture-Transfer.git
	cd Picture-Transfer
 	python -m venv .venv 
 	source .venv/bin/activate
 	pip install -r requirements.txt
 	cd experiments  
	```
0. Camera Demo
	```bash
	python camera_demo.py demo --model models/21styles.model
	```
	![](images/myimage.gif)
0. Test the model
	```bash
	python main.py eval --content-image images/content/venice-boat.jpg --style-image images/21styles/candy.jpg --model models/21styles.model --content-size 1024
	```
	```bash
	python main.py eval --content-image images/content/summer.jpg --style-image images/21styles/starry_night.jpg --model models/21styles.model --output-image my_images/summer_output.jpg
	```
* If you don't have a GPU, simply set `--cuda=0`. For a different style, set `--style-image path/to/style`.
	If you would to stylize your own photo, change the `--content-image path/to/your/photo`. 
	More options:

	* `--content-image`: path to content image you want to stylize.
	* `--style-image`: path to style image (typically covered during the training).
	* `--model`: path to the pre-trained model to be used for stylizing the image.
	* `--output-image`: path for saving the output image.
	* `--content-size`: the content image size to test on.
	* `--cuda`: set it to 1 for running on GPU, 0 for CPU.

<img src ="images/1.jpg" width="260px" /> <img src ="images/2.jpg" width="260px" />
<img src ="images/3.jpg" width="260px" />
<img src ="images/4.jpg" width="260px" />
<img src ="images/5.jpg" width="260px" />
<img src ="images/6.jpg" width="260px" />
<img src ="images/7.jpg" width="260px" />
<img src ="images/8.jpg" width="260px" />
<img src ="images/9.jpg" width="260px" />

### Train Your Own MSG-Net Model
0. Download the COCO dataset
	```bash
	bash dataset/download_dataset.sh
	```
0. Train the model
	```bash
	python main.py train --epochs 4
 	python main.py train --epochs 4 --style-folder ./images/21styles/ --cuda 0
	```
* If you would like to customize styles, set `--style-folder path/to/your/styles`. More options:
	* `--style-folder`: path to the folder style images.
	* `--vgg-model-dir`: path to folder where the vgg model will be downloaded.
	* `--save-model-dir`: path to folder where trained model will be saved.
	* `--cuda`: set it to 1 for running on GPU, 0 for CPU.

## Neural Style

[Image Style Transfer Using Convolutional Neural Networks](http://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf) by Leon A. Gatys, Alexander S. Ecker, and Matthias Bethge.

```bash
python main.py optim --content-image images/content/venice-boat.jpg --style-image images/21styles/candy.jpg --output-image my_images/venice_boat_output.jpg
```
* `--content-image`: path to content image.
* `--style-image`: path to style image.
* `--output-image`: path for saving the output image.
* `--content-size`: the content image size to test on.
* `--style-size`: the style image size to test on.
* `--cuda`: set it to 1 for running on GPU, 0 for CPU.

<img src ="images/g1.jpg" width="260px" /> <img src ="images/g2.jpg" width="260px" />
<img src ="images/g3.jpg" width="260px" />
<img src ="images/g4.jpg" width="260px" />
<img src ="images/g5.jpg" width="260px" />
<img src ="images/g6.jpg" width="260px" />
<img src ="images/g7.jpg" width="260px" />
<img src ="images/g8.jpg" width="260px" />
<img src ="images/g9.jpg" width="260px" />

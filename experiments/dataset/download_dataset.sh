cd dataset
# Download COCO 2014 dataset
wget http://images.cocodataset.org/zips/train2014.zip
wget http://images.cocodataset.org/zips/val2014.zip

# Unzip the files
unzip train2014.zip
unzip val2014.zip

# Clean up zip files
rm *.zip
cd ..

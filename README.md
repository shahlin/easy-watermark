# Easy Watermark
Easy watermark reduces the pain to manually add watermarks to your images and automatically adds it for you. Lets say you have a 100 images and want to watermark all of them. Just use this tiny program!

## Prerequisities
- Python

## Example
![alt text](https://i.imgur.com/Gwf6d9O.jpg)
Watermarked using the program

## Running the program
- Step 0, download the repository and open a console inside the folder, setup a virtual environment and activate it.
- First step is to download the required dependencies. To do that, run the following command on your console:
   ```
   pip install -r requirements.txt
   ```
- After that, you're ready to run the program. Well, almost. You need to make sure you have a watermark image. You can either name it **watermark.png** and place it in the repository folder. In that case, run the following command:
   ```
   python app.py images/test.jpg  # Can specify a single image or a folder with images
   ```
- Or you can use the command line option to specify the watermark path. Example:
   ```
   python app.py images/test.jpg -w path/to/my_watermark.png
   ```
## Command line arguments
- **image** or **images folder** path

   This is a mandatory argument specified after the _python app.py_. It accepts a path to an image or it can be a path to a folder which supposedly contains pictures. Example:
   ```
   python app.py images/test.jpg
   ```
   ```
   python app.py images
   ```
- **-w, --watermark**

   This option lets you specify the path to your watermark image. If this option is not specified, the default is taken to be 'watermark.png' file in the current directory. Make sure its a .png image. Example:
    ```
    python app.py images -w path/to/my_watermark.png
    ```
    ```
    python app.py images --watermark path/to/my_watermark.png
    ```
- **-p, --position**

   This option lets you specify the position where the watermark is to be placed. Can be one of the four: topleft, topright, bottomleft, bottomright. By default, it is set to bottomright. Example:
    ```
    python app.py images -p topright
    ```
    ```
    python app.py images --position bottomright
    ```
- **-s, --size**

   This option lets you specify the size of the watermark. The automatically set size might not be correct or not as expected. Hence, the size option lets you specify a width and height for your watermark. If only 1 number is specified, it'll be applied for both width and height. Example:
    ```
    python app.py images -s 128
    ```
    ```
    python app.py images --size 128 140
    ```
- **-o, --output**

   This option lets you specify the folder where the final output is stored. By default it creates an output directory in the current folder. Example:
    ```
    python app.py images -o my_output_dir
    ```

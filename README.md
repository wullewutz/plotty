# plotty - realtime (embedded) data visualization made easy

![plotty at work](docs/screencast.gif)

* Ever wanted to inspect some sensor data captured by your arduino or other embedded system in realtime?
* Ever wanted to fine-tune a PID controller but couldn't understand why it keeps oscillating?
* Ever wanted to have a look at some recored .csv data but $YOUR_#!"#_SPREADSHEET_APP just sucks at zooming into details?

plotty might just be what you've been looking for.

## basic usage

To have a quick look at plotty, just clone the repo and make sure you've installed
the dependencies listed below.
Then start plotty in simulation mode:
```
cd plotty
python plotty
```
* Move the plott area with your left mouse button.
* Zoom into details with your mouse wheel.
* Fancy X and Z axis zooming with your right mouse button - try it!
* Reset to normal by clicking on the small "A" at the bottom left if you got lost in your data ;)

## configuration

To make plotty plot real life data generated by your dev-board, just dump the data continuously as
space-separated float values through your serial debug shell using some code on the embedded side like this:

```
printf("%f %f %f\n", valueA, valueB, valueC);
```

In the plotty directory, edit config.json to suit your needs:
```
{
    "inputStream": "simulation",
    "baud": 921600,
    "sampleRate": 1000,
    "bufferSize": 10000,
    "channels":
    [
	{"legend": "Temp[°C]",       "color": "orange"},
	{"legend": "Pressue[hPa]",   "color": "green"},
	{"legend": "Humidity[%rel]", "color": "cyan"}
    ]
}
```
* Replace `"simulation"` with your actual serial data source for example `"/dev/ttyUSB0"` on Linux or `"COM3"` on Windows.
* The `"baud"`-rate has only to be specified correcly on Windows.
* `"sampleRate"` is the number of lines you transmit per second.
* `"bufferSize"` is the depth of data buffer of each channel. Reduce this, if your PC is to slow...
* In the `"channels"` section, you specifiy the `"legend"`-string to be printed in your plot and the `"color"` of the plotted line (for each channel).

You can add or remove channels to suite your needs by adding or removing lines from the `"channels"` list.
Currently, the following colors are supported: yellow, orange, red, magenta, violet, blue, cyan, green.

## static data analysis

If you just want to have a look at a huge set of data like an exported .csv file, just point to the file
```
...
    "inputStream": "./testdata.csv"
...
```
NOTE: To plot files, the data has to be space separated floating point values.
Make sure to not have more values per line than channels configured in your config.json.

## dependencies

python3
pyqtgraph
pyqt4
numpy
pyserial (required on Windows only)

## credits
* Ethan Schoonover for creating the famous [solarized color pallete](http://ethanschoonover.com/solarized)
* Luke Campagnola for [pyqtgraph](https://github.com/pyqtgraph/pyqtgraph)

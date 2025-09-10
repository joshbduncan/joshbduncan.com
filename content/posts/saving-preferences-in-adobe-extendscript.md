---
title: Saving JSON "like" Preferences Files With Adobe ExtendScript
date: 2022-07-07
description: Some of my scripts for Adobe products have the ability to save user preferences. Here's how I save those preferences to a JSON like file on disk using ExtendScript and the Adobe Bridge Messaging API.
author: Josh Duncan
category: development
tags: adobe, extendscript, javascript
---

Any time I'm writing an [Adobe ExtendScript](https://extendscript.docsforadobe.dev/introduction/extendscript-overview.html) that includes a dialog box with more than a few options, I like to give the user the ability to save their dialog selections to a preference file. That way, when they run the script again their defaults (or last used settings) are preloaded, saving them time.

I hope to go deeper into this subject in a later post, but for now I'll show you how I write the users last used settings out to a JSON "like" file on their hard disk.

## What is JSON "like"?

Adobe ExtendScript doesn't include a JSON library, so to easily read and write JSON I'll be using the [Adobe Bridge Messaging API](https://extendscript.docsforadobe.dev/interapplication-communication/communicating-through-messages.html). This API provides two key functions.

- `toSource()` to serialize/encode JavaScript [objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects) and [arrays](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)
- `eval()` to reconstitute/decode JavaScript objects and arrays

The reason I say JSON "like" is because the `toSource()` function doesn't encode valid JSON, it serializes objects or arrays into a special string. There are a few funky aspects of this serialized string that make it invalid JSON, but since I'll be reconstituting it using the `eval()` function, it works perfect for my purposes.

```javascript
// valid json
{
	"a": 1,
	"b": 2
}

// invalid `toSource()` serialized JSON string
({"a": 1, "b": 2})
```

*Going forward, I'll just use the term JSON.*

## Script Setup

First, I'll setup some option variables that will be used to create the dialog window, and I'll also set defaults to be used on the first run (or when a preferences file isn't found).

```javascript
var locations = ["Location 1", "Location 2", "Location 3"];
var products = ["Product 1", "Product 2", "Product 3"];
var defaults = { location: "Location 1", product: "Product 3" };
```

Next, I'll check to see if a preferences file already exists. To do this, I make a new [File object](https://extendscript.docsforadobe.dev/file-system-access/file-object.html) pointing at the user’s default document folder path provided by ExtendScript's [Folder object](https://extendscript.docsforadobe.dev/file-system-access/folder-object.html?highlight=folder#folder-class-properties) class properties `Folder.myDocuments`.

```javascript
var prefsFile = new File(Folder.myDocuments + "/prefs.json");
var prefsData = prefsFile.exists ? readJSONData(prefsFile) : defaults;
```

Using a [Conditional (ternary) operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Conditional_Operator) I'll set `prefsData` to the data read from `prefsFile` (if it exists) using the `readJSONData()` function below, or to the defaults I set above.

## Reading JSON Files With ExtendScript

Reading the JSON data from the preferences file is pretty straight forward. First, I try opening the file and reading its data to the variable `json`. If all is successful, I'll reconstitute/decode that data back into a JavaScript object (using the [`eval()`](https://extendscript.docsforadobe.dev/interapplication-communication/communicating-through-messages.html?highlight=toSource#passing-an-object-with-tosource-and-eval) function mentioned above) and return it for use in the dialog window.

```javascript
function readJSONData(file) {
  var obj, json;
  try {
    file.encoding = "UTF-8";
    file.open("r");
    json = file.read();
    file.close();
  } catch (e) {
    alert("Error loading " + file + " file!");
  }
  obj = eval(json);
  return obj;
}
```

## Presenting The Dialog

I won't go into too much detail in this post on the dialog creation code, but basically I create a simple dialog full of radio buttons determined by the `locations` and `products` arrays from above.

Now, the reason for all of this work is that while creating the radio buttons (or most any UI element), I can check to see if a particular element (radio button) is set in the `prefsData` object (be it either loaded from a file or the defaults), and if so, preselect if for the user. As you can see, this can be a huge timesaver if a dialog has lots of options or if the user needs the ability to save multiple presets for different uses.

![Save Preferences From Dialog Example](/static/images/save-preferences-adobe-extendscript-dialog.png){: loading="lazy" }

```javascript
// show the settings dialog
var settings = settingsWin(prefsData);
// parse the dialog settings
if (settings) {
  alert(
    "User Settings Saved!\nSelected Location: " +
      settings.location +
      "\nSelected Product: " +
      settings.product
  );
}

// get selected radio button from array
function captureRBSelection(rbs) {
  for (var i = 0; i < rbs.length; i++) {
    if (rbs[i].value) return rbs[i].text;
  }
  return null;
}

// setup the dialog window
function settingsWin(prefsData) {
  var win = new Window("dialog");
  win.text = "Save Preferences From Dialog Example";

  // create a radio button for each location
  win.add("statictext", undefined, "Select Your Location");
  var gLocation = win.add("group");
  var locationRBs = [];
  var rb;
  for (var i = 0; i < locations.length; i++) {
    rb = gLocation.add("radiobutton", undefined, locations[i]);
    if (prefsData["location"] == locations[i]) rb.value = true;
    locationRBs.push(rb);
  }

  // create a radio button for each product
  win.add("statictext", undefined, "Select Your Product Type");
  var gProducts = win.add("group");
  var productRBs = [];
  var rb;
  for (var i = 0; i < products.length; i++) {
    rb = gProducts.add("radiobutton", undefined, products[i]);
    if (prefsData["product"] == products[i]) rb.value = true;
    productRBs.push(rb);
  }

  // setup window buttons
  var gWindowButtons = win.add("group", undefined);
  var btOK = gWindowButtons.add("button", undefined, "OK");
  var btCancel = gWindowButtons.add("button", undefined, "Cancel");

  // if "ok" button clicked then return inputs
  if (win.show() == 1) {
    // check to see which location and product was selected
    var selectedSettings = {
      location: captureRBSelection(locationRBs),
      product: captureRBSelection(productRBs),
    };
    return selectedSettings;
  } else {
    return;
  }
}
```

The main thing to understand from the code above are the final few lines. If the user clicks the "OK" button `if (win.show() == 1)`, I gather their dialog selections (radio buttons in this case) and construct an object from them that I can return for use in the rest of the script.

<<< .callout
You may notice a utility function above called `captureRBSelection()`. It's not necessarily needed, it just provides an easy way to determine which radio button from a UI group is selected. 
>>>

## Writing JSON Files With ExtendScript

Now that I have the user selected settings from the dialog stored as an object, I can write that data to the preferences file.

```javascript
if (settings) {
  writeJSONData(settings, prefsFile);
}
```

Writing the JSON data to a file is not that dissimilar from reading it. First, I serialize the JSON data using the [`toSource()`](https://extendscript.docsforadobe.dev/interapplication-communication/communicating-through-messages.html?highlight=toSource#passing-an-object-with-tosource-and-eval) function mentioned above. Then, I try writing the data to disk using the [`write()`](https://extendscript.docsforadobe.dev/file-system-access/file-object.html#write) function provided by the file object.

```javascript
function writeJSONData(obj, file) {
  var data = obj.toSource();
  try {
    file.encoding = "UTF-8";
    file.open("w");
    file.write(data);
    file.close();
  } catch (e) {
    alert("Error writing file " + file + "!");
  }
}
```

<<< .callout
Normally, a script would do more than just write a preferences file. Usually, the selection(s) made by the user direct the next steps the script takes. In this case, that only means showing the selected preferences in an alert.
>>>

```javascript
alert(
  "User Settings Saved!\nSelected Location: " +
    settings.location +
    "\nSelected Product: " +
    settings.product
);
```

![Save Preferences Alert](/static/images/save-preferences-adobe-extendscript-dialog-alert.png){: loading="lazy" }

## Final Thoughts

This setup is just the base for more advanced functionality like I implemented in my [Screen Print Separation Marks](https://github.com/joshbduncan/adobe-scripts/blob/main/ScreenSepMarks.jsx) script shown below. I hope to do a more in-depth post on this in the future.

![Save Preferences From Dialog Advanced](/static/images/save-preferences-adobe-extendscript-dialog-advanced.png){: loading="lazy" }

View the [full script](https://github.com/joshbduncan/adobe-scripts/blob/main/snippets/savePrefsFromDialog.jsx) on Github. ✌️

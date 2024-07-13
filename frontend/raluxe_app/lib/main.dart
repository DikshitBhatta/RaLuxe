import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ImageCaptureScreen(),
    );
  }
}

class ImageCaptureScreen extends StatefulWidget {
  @override
  _ImageCaptureScreenState createState() => _ImageCaptureScreenState();
}

class _ImageCaptureScreenState extends State<ImageCaptureScreen> {
  File? _image;
  bool _isFilterApplied = false;

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.getImage(source: ImageSource.camera);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
        _isFilterApplied = false; // Reset filter status
      });
    }
  }

  Future<File> _processImageWithMoustacheFilter(File imageFile) async {
    final uri = Uri.parse('http://127.0.0.1:8000/image/process');
    var request = http.MultipartRequest('POST', uri);
    request.files
        .add(await http.MultipartFile.fromPath('image', imageFile.path));

    var response = await request.send();
    if (response.statusCode == 200) {
      var responseData = await response.stream.toBytes();
      var decoded = json.decode(String.fromCharCodes(responseData));
      return File(decoded['image']);
    } else {
      throw Exception('Failed to process image');
    }
  }

  Future<void> _applyMoustacheFilter() async {
    if (_image == null) return;

    try {
      File filteredImage = await _processImageWithMoustacheFilter(_image!);
      setState(() {
        _image = filteredImage;
        _isFilterApplied = true;
      });
    } catch (e) {
      print('Error applying moustache filter: $e');
      // Handle error, show message to user, etc.
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('RaLuxe App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _image == null
                ? Text('No image selected.')
                : Stack(
                    alignment: Alignment.center,
                    children: [
                      Image.file(_image!),
                      if (_isFilterApplied)
                        Image.file(_image!), // Display filtered image
                    ],
                  ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: Text('Pick Image'),
            ),
            ElevatedButton(
              onPressed: _applyMoustacheFilter,
              child: Text('Apply Moustache Filter'),
            ),
          ],
        ),
      ),
    );
  }
}

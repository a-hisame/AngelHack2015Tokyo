<html>
<head><title>Upload Test</title></head>
<body>
  <p>Upload Images</p>
  <form action="/hungry/api/upload" method="post" enctype="multipart/form-data">
    Name: <input type="text" name="name" /> <br>
    Tags: <input type="text" name="tags" /> <br>
    Location(Restaurant): <input type="text" name="location" /> <br>
    ImageFile: <input type="file" name="upload" /> <br>
    <input type="submit" value="Start upload" />
  </form>
</body>
</html>


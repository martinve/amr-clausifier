<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Logicparser</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.2.1/dist/flatly/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/app.css">
    <style>
        code {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-sm ">
    <div class="container">
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/">Home</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/import">Import</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/parse">Parse</a>
      </li>
        </li>
        <li class="nav-item">
        <a class="nav-link" href="/resources">Resources</a>
      </li>
          <li class="nav-item">
        <a class="nav-link" href="/flush">Recreate</a>
      </li>
    </ul>
  </div>
  </nav>
</nav>

<div class="container{{get("container_extra", "")}}"">
    {{!base}}
</div>

</body>
</html>
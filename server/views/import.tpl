% rebase('base.tpl', title='Page Title')

<h1>Import Experiment</h1>

<form method="post" action="/import" enctype="multipart/form-data">
    <input type="file" name="upfile">
    <input type="submit" value="Upload file">
</form>


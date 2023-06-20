% rebase('base.tpl', title='Parse Passage')

<h1>Parse Passage</h1>

<form method="post" action="/parse">
    %if "passage" in locals():
        <a href="/passage/{{passage.id}}">Back</a>
    <input type="hidden" name="passage_id" value="{{passage.id}}">
    %end
    <div class="form-group">
        <label for="passage">Passage</label>
        <textarea class="form-control" id="passage" name="passage" rows="20"></textarea>
    </div>
    <button type="submit" class="btn btn-outline-primary mt-2">Parse passage</button>
</form>

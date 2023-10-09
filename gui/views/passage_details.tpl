% rebase('base.tpl', title="Experiment Details")

<h1>Passage Parse</h1>

<div>
Cache file name: {{passage.filename}}
</div>


<a class="btn btn-outline-info btn-sm" href="/passage/{{passage.id}}/add">Add sentence</a>
<a class="btn btn-outline-info btn-sm" href="/passage/{{passage.id}}/sentences">Sentence output</a>
<a class="btn btn-outline-danger btn-sm" href="/passage/{{passage.id}}/delete">Delete passage</a>



<table class="table table-hover">
    <tbody>
        % for row in passage.sentences:
        <tr>
            <td>
                <a class="btn btn-outline-success btn-sm" href="/sentences/{{row.id}}">Show</a> {{ row.text }}
            </td>
            <td>
                <a class="btn btn-outline-success btn-sm" href="/sentences/{{row.id}}/delete">Delete</a>
            </td>
        </tr>
        %end
    </tbody>
</table>
% rebase('base.tpl', title="Experiment Details")

<h1>Passage Parse</h1>

<table class="table table-hover">

    <a href="/passage/{{passage.id}}/add">Add sentence</a>

    <a href="/passage/{{passage.id}}/sentences">Sentence output</a>

    <a href="/passage/{{passage.id}}/delete">Delete passage</a>

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
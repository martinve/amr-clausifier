% rebase('base.tpl', title="All Sentences", container_extra="fluid")
% import formatter

% from udutil import format_ud
% import pickle



<h1>All Sentences</h1>

<a href="/sentences/refresh">Rebuild Contexts</a>

<table class="table table-bordered table-hover">

    <tbody>
        % for sentence in sentences:
        <tr>
            <td>
                <a class="btn btn-outline-success btn-sm" href="/sentences/{{sentence.id}}">Show</a> {{ sentence.text }}
            </td>
            <td>
                <code>{{ sentence.parse_amr }}</code>
            </td>
            <td>
                <code>{{ "\n".join(format_ud(pickle.loads(sentence.parse_ud))) }}</code>
            </td>
            <!--
            <td>
                <code>{{ formatter.format_json(sentence.context) }}</code>
            </td>
            -->
            <td>
                <code>{{ formatter.format_logic(sentence.simpl_logic) }}</code>
            </td>
        </tr>
        %end
    </tbody>
</table>
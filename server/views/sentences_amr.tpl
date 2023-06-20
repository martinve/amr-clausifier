% rebase('base.tpl', title="All Sentences", container_extra="fluid")
% import formatter

% from udutil import format_ud
% import pickle





<h1>All Sentences</h1>

<a href="/sentences/refresh">Rebuild Contexts</a>

% for sentence in sentences:
    <br>
    <code>{{ sentence.parse_amr }}</code>
%

<!--
<table class="table table-bordered table-hover">

    <tbody>
        % for sentence in sentences:
        <tr>
            <td>
                {{ sentence.text }}
            </td>
            <td>
                <code>{{ sentence.parse_amr }}</code>
            </td>
        </tr>
        %end
    </tbody>
</table>
-->
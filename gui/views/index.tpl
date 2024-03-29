% rebase('base.tpl', title='Page Title')

% from view_formatter import truncate

<h1>Past Experiments</h1>

Total: {{ len(rows) }}

% if len(rows) > 0:

    <table class="table table-hover">
        <tbody>
    % for row in rows:
        <tr>
            <td>{{ truncate(row.passage) }}</td>
            <td><a class="btn" href="/passage/{{ row.id }}">Details</a>
        </tr>
    % end
        </tbody>
    </table>
% end

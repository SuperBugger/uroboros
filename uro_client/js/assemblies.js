$(document).ready(function(){
    var project_name = window.location.pathname.split('/')[1];
    $.ajax({
        url: `http://127.0.0.1:5000/${project_name}/get_assemblies`,
        type: 'GET',
        success: function(response) {
            if(response.assemblies) {
                var assemblies = response.assemblies;
                var tbody = $('#assembliesTable tbody');
                tbody.empty();

                assemblies.forEach(function(assembly) {
                    var row = `<tr>
                        <td>${assembly.assm_id}</td>
                        <td>${assembly.assm_date_created}</td>
                        <td>${assembly.assm_desc}</td>
                        <td>${assembly.assm_version}</td>
                    </tr>`;
                    tbody.append(row);
                });
            } else {
                console.error('No assemblies found in response');
            }
        },
        error: function(error) {
            console.error('Error fetching assemblies:', error);
        }
    });
});

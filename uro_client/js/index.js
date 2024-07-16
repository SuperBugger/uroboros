$(function () {
    $("#example1").DataTable({
        "responsive": true, "lengthChange": false, "autoWidth": false,
        "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"]
    }).buttons().container().appendTo('#example1_wrapper .col-md-6:eq(0)');
});
document.querySelectorAll('.sidebar ul li a').forEach(item => {
    item.addEventListener('click', event => {
        event.preventDefault();
        const targetId = event.target.getAttribute('data-target');
        document.querySelectorAll('section').forEach(section => {
            section.style.display = 'none';
        });
        document.getElementById(targetId).style.display = 'block';
    });
});
$(document).ready(function () {
    $.ajax({
        url: 'http://127.0.0.1:5000/get_projects',
        type: 'GET',
        success: function (response) {
            if (response.projects) {
                var projects = response.projects;
                var tbody = $('#example1 tbody');
                tbody.empty();

                projects.forEach(function (project) {
                    var row = `<tr data-href="/${project.prj_name}/assemblies">
                                <td>${project.prj_name}</td>
                                <td>${project.arch_name}</td>
                                <td>${project.rel_name}</td>
                                <td>${project.vendor}</td>
                                <td>${project.prj_desc}</td>
                            </tr>`;
                    tbody.append(row);
                });

                $('#example1 tbody').on('click', 'tr', function () {
                    var $this = $(this);
                    if ($this.hasClass('selected')) {
                        window.location.href = $this.data('href');
                    } else {
                        $('#example1 tbody tr').removeClass('selected');
                        $this.addClass('selected');
                    }
                });
            } else {
                console.error('No projects found in response');
            }
        },
        error: function (error) {
            console.error('Error fetching projects:', error);
        }
    });
});

// assemblies.js
$(document).ready(function(){
    var project_name = "{{ project_name }}";
    $.ajax({
        url: `http://127.0.0.1:5000/${project_name}/assemblies`,
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

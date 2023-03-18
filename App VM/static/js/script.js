// All the JavaScript functions for datatable and other calls are defined here
//Defining the datatable.
jQuery(document).ready(function($){
    $('#myTable').DataTable( {
        columns: [                  //Defining table structure. Must align with the database collection structure
            { data: 'emp_id' },
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'ph_no' },
            { data: 'home_addr' },
            { data: 'st_addr' },
            { data: 'gender' },
            { data: 'job_type' },
            { data: 'edit'},
            { data: 'delete'},
        ],
        searching: true,
        //select: "single", // Use this to select a single row and take action on that
        "autoWidth": false,
        responsive: true,
        //fixedColumns: true,
        fixedHeader: true,
    } );
    
    

    // Handling the edit function
    // This will activate when the edit button in the table row clicked
    $("#myTable").on("click", ".edit-button", function(){  
        $tr = $(this).closest('tr');
        // Popup modal when clicking on the Edit icon
        $(".modal-body div span").text("");
        $(".emp_id span").text($( $tr[0].cells[0]).text());
        
        // Getting the default value of the row items (fields)
        // document.getElementById("edit-emp_id").value = $('.emp_id', $tr).text();
        document.getElementById("edit-first_name").value = $('.first_name', $tr).text();
        document.getElementById("edit-last_name").value = $('.last_name', $tr).text();
        document.getElementById("edit-ph_no").value = $('.ph_no', $tr).text();
        document.getElementById("edit-home_addr").value = $('.home_addr', $tr).text();
        document.getElementById("edit-st_addr").value = $('.st_addr', $tr).text();
        document.getElementById("edit-gender").value = $('.gender', $tr).text();
        document.getElementById("edit-job_type").value = $('.job_type', $tr).text();
        
        $("#myEditModal").modal("show");  // Showing the myEditModal defined in the modals.html

        $('#edit_record_button').on('click', function(){  
            $("#myEditModal").modal("hide");

            // Getting the updated value of the row items (fields)
            var emp_id = $( $tr[0].cells[0]).text() // non-editable, so taking the default value of emp_id
            var first_name = $('#edit-first_name').val(); 
            var last_name = $('#edit-last_name').val();
            var email = first_name + '.' + last_name + '@acme.com';
            var ph_no = $('#edit-ph_no').val();
            var home_addr = $('#edit-home_addr').val(); 
            var st_addr = $('#edit-st_addr').val(); 
            var gender = $('#edit-gender').val(); 
            var job_type = $('#edit-job_type').val(); 
            //alert("Reached till this end. Got the new data");

            // Fields mentioned below cannot be empty
            if(emp_id != '' && first_name != '' && last_name != '' && ph_no != '' && job_type != '')  
            {  
                $.ajax({  
                    url:"/employee/"+ $( $tr[0].cells[0]).text(),  
                    // method:"POST",  
                    method:"PUT",
                    data: {emp_id:emp_id, first_name:first_name, last_name:last_name, email:email, ph_no:ph_no, home_addr:home_addr, st_addr:st_addr, gender:gender,job_type:job_type},  
                    success:function(data)  
                    {  
                        alert(data);  
                        if(data == 'No-data')  
                        {  
                            alert("Invalid Records!");  
                        }  
                        else
                        {  
                            $('#myEditModal').hide();  
                            location.reload();  
                        }  
                    }  
                });  
            }  
            else
            {  
                    alert("All Fields are required");  
            }    
            
        });  
        //alert("You want to edit: Record ID " + $('.id', $tr).text() + " & Artist: " + $('.artist', $tr).text());     
        //You can use this info and set it to the inputs with javascript: $("edit_category_modal input[type='text']").val($('.category-name', $tr).text()) for example;
    });

    // Handling the delete function

    $("#myTable").on("click", ".delete-button", function(){
        $tr = $(this).closest('tr');
        // Popup modal when clicking on the delete icon
        
        $(".modal-body div span").text("");
        $(".emp_id span").text($( $tr[0].cells[0]).text());
        $(".first_name span").text($('.first_name', $tr).text());
        $(".last_name span").text($('.last_name', $tr).text());
        $(".email span").text($('.email', $tr).text());
        $(".ph_no span").text($('.ph_no', $tr).text());
        $(".home_addr span").text($('.home_addr', $tr).text());
        $(".st_addr span").text($('.st_addr', $tr).text());
        $(".gender span").text($('.gender', $tr).text());
        $(".job_type span").text($('.job_type', $tr).text());
        $("#myDeleteModal").modal("show");
        //alert("You want to edit: Record ID " + $('.id', $tr).text() + " & Artist: " + $('.artist', $tr).text());     
        //You can use this info and set it to the inputs with javascript: $("edit_category_modal input[type='text']").val($('.category-name', $tr).text()) for example;

        // Delete the Record
        $('#delete_record_button').on('click', function(){  
            $("#myDeleteModal").modal("hide");
            $.ajax({  
                // url:"/delete/"+ $( $tr[0].cells[0]).text(), 
                url:"/employee/"+ $( $tr[0].cells[0]).text(), 
                //method:"POST",  
                method:"DELETE",
                success:function(data)  
                {  
                    alert(data);  
                    if(data == 'No-data')  
                    {  
                        alert("Invalid Records!");  
                    }  
                    else
                    {  
                        $('#myDeleteModal').hide();  
                        location.reload();  
                    }  
                }  
            });  
            
        });  
        
    });

// Adding an employee information to the database
    $('#add_record_button').click(function(){  
        var table = $('#myTable').DataTable(); // Getting total number of rows in the table which is equal to no. of employees
 
        var emp_id = table.data().count() + 1; //Getting the next number in the number of employees
        var first_name = $('#first_name').val(); 
        var last_name = $('#last_name').val();
        var email = first_name + '.' + last_name + '@acme.com';
        var ph_no = $('#ph_no').val();
        var home_addr = $('#home_addr').val(); 
        var st_addr = $('#st_addr').val(); 
        var gender = $('#gender').val(); 
        var job_type = $('#job_type').val(); 
        

        if(emp_id != '' && first_name != '' && last_name != '' && ph_no != '' && job_type != '')  
        {  
                $.ajax({  
                    url:"/employee",  
                    method:"POST",  
                    data: {emp_id:emp_id, first_name:first_name, last_name:last_name, email:email, ph_no:ph_no, home_addr:home_addr, st_addr:st_addr, gender:gender,job_type:job_type},  
                    success:function(data)  
                    {  
                        alert(data);  
                        if(data == 'No-data')  
                        {  
                            alert("Invalid Records!");  
                        }  
                        else
                        {  
                            $('#addModal').hide();  
                            location.reload();  
                        }  
                    }  
                });  
        }  
        else
        {  
                alert("All Fields are required");  
        }  
    }); 
});

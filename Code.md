# Technical Overview

This document exaplains some pieces of code for future reference of the project.

## Project Structure

The project is structured such that the entire app is placed inside the folder and only the _run.py_ file is kept outside the folder. This is done to remove cyclic import errors. This is used to make the app into a module.

_init.py_ contains the initialization attributes of the entire project. The details regarding the project like the environment variables are present here. 

_The project has been made into single thread. When a solution for multi-threading architecture is known, it is to be implemented_

## AJAX request in search page

```
$(document).ready(function(){

  $("form#HP-list").on('submit',function(event){

    event.preventDefault();

    var data = 10;

    var fieldPair = '';
    $("form#HP-list :input").each(function(){
      fieldPair += $(this).attr("name") + ':'
      var name = String($(this).attr("name"));
      if(name.includes('csrf'))
      {
        fieldPair+= ';';
      }
      else{
        if(name.includes('select')){
          fieldPair += $(this).find(':selected').text();
          fieldPair+= ';';
        }
        else{
          fieldPair += $(this).is(":checked");
          fieldPair+= ',';
        } 
      }    
    });
    
    req = $.ajax({

      url: '/bg_process',
      type: 'POST',
      data:{
        test:data,
        clf:$("#task-select").find(":selected").text(),
        form_data:fieldPair,
      },
      success:function(response){
        $('#results-replacement').empty()
        $('#results-replacement').append(response.data)
      }
    });

  })


})
```

The above function is written in jQuery. The gist of the function is to prevent the default submit action.  Serialize all the fields using the .each function. The key value pairs are seperated by **;** and the key - values are seperate by a **,**. 

ajax request is made to the route created with bg_process which only accepts POST requests. The data sent to the route is used to filter the search results. On successfully returning the value, the entire part of the page (DOM) corresponding to results will be disappearred. The template returned from the ajax request will be used in the place.

## _SQLfns.py_ file

Some of the functions related to SQL are written in this file which is used in the code. This is file is like a utilities file which is used to accomplish a task.

## _sqltables.py_ file

This file contains some code to automatically create and access tables from sql database. These are the related codes online which can be used to automate creation and accessing of tables and data. This file is not being used.

## _InjectData.py_ file

A file to inject data into tables by using the tablenames. All the functions required to identify and inject the data is present in this file.  Currently this file is being used in injection of csv data.

## _InjectFromCSV.py_ file 

This file contains boilerplate code which is not intelligent in determining the required table automatically. This file is not being used currently. This file acts as backup, if the injectdata.csv file fails.



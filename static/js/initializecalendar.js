$(document).ready(function() {
    
//
//    TODO
//    make an AJAX call to get a JsonResponse from the server containing all the data about the tournaments pulled from the *DATABASE*
//

    $('#calendar').fullCalendar({
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,basicWeek,basicDay'
      },
      defaultDate: '2021-3-01',
      navLinks: true, // can click day/week names to navigate views
      editable: true,
      eventLimit: true, // allow "more" link when too many events
	  
      events: [
        {
          title: 'All Day Event',
          start: '2021-3-01'
        },
        {
          title: 'Tournament1',
          start: '2021-3-08T14:00:00' // remove all static data, populate events in views.py with the tournaments from database
        },
		{
          title: 'Tournament2',
          start: '2021-3-20',
		  end: '2021-3-25'
        },
		{
          title: 'Tournament3',
          start: '2021-4-10'
        }
      ]
    }); 
  });
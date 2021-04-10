$(function() {
  $.get('/chess/update-calendar/', function(data) {
    var calendar_setup = {
      themeSystem:'bootstrap3',
      headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
          },
      initialDate: Date.now(),
      navLinks: true, // can click day/week names to navigate views
      dayMaxEvents: true,
      events: data}
    
    var calendar = new FullCalendar.Calendar($('#calendar').get(0), calendar_setup);
    calendar.render();
  }); 
});
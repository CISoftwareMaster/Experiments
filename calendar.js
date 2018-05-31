function animated_scroll(y, target, speed)
{
    if ((speed > 0 ? y < target : y > target))
    {
        window.scroll(0, y);
        setTimeout(`animated_scroll(${y + speed}, ${target}, ${speed})`, 0);
    }
}

window.onload = function(e)
{
    // get reference to our Calendar wrapper node
    var calwrap = document.getElementById("calendar");

    // get reference to our message box UI elements
    var message_box = document.getElementById("messageBox");
    var message_title = document.getElementById("mboxTitle");
    var message_body = document.getElementById("mboxBody");
    var overlay = document.getElementById("overlay");

    // have we generated a calendar yet?
    var cal_generated = false;

    // a list containing our month names
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    // leap year check function
    function is_leap(year)
    {
        if ((year % 4) == 0)
        {
            if ((year % 100) == 0)
            {
                if ((year % 400) == 0)
                    return true;
            }
            else
            {
                return true;
            }
        }
        return false;
    }

    function days_in_month(m, y)
    {
        // non February months
        if (m != 2)
        {
            var x = (m % 2);
            return (m < 8 ? 30 + x : 31 - x);
        }

        return (is_leap(y) ? 29 : 28);
    }

    // our message box functionality
    function show_message(title, message)
    {
        // show our overlay
        var transform = "translate(0, 0)";
        overlay.style.opacity = "1";
        overlay.style.webkitTransform = transform;
        overlay.style.transform = transform;

        // update our message box components
        message_title.innerText = title;
        message_body.innerText = message;

        // show our message box
        var transform_2 = "translate(-50%, -50%)";
        message_box.style.opacity = "1";
        message_box.style.webkitTransform = transform_2;
        message_box.style.transform = transform_2;
    }

    function hide_message()
    {
        // hide our overlay
        var transform = "translate(0, -100%)";
        overlay.style.opacity = "0";
        overlay.style.webkitTransform = transform;
        overlay.style.transform = transform;

        // hide our message box
        var transform_2 = "translate(-50%, 100%)";
        message_box.style.opacity = "0";
        message_box.style.webkitTransform = transform_2;
        message_box.style.transform = transform_2;
    }

    // handle calendar generation
    document.getElementById("generate").onclick = function(e)
    {
        // check if a Calendar DOM already exists
        if (document.getElementById("calendarDOM"))
        {
            var tref = document.getElementById("calendarDOM");
            // delete it
            calwrap.removeChild(tref);
            delete tref;
        }

        // get our input variables
        var start_date = Number(document.getElementById("startYear").value);
        var end_date = Number(document.getElementById("endYear").value);

        // apply our constraints
        if (start_date >= end_date || end_date < 1001 || start_date < 1000)
        {
            // reset our generation status
            cal_generated = false;
            // show warning
            show_message("Error", "You have set an invalid date range");
            // cancel operations
            return;
        }

        // reference to our Calendar DOM node
        var calendar = document.createElement("div");
        calendar.setAttribute("id", "calendarDOM");

        // get our current date
        var date = new Date();

        // generate our calendar
        for (var year = start_date; year <= end_date; ++ year)
        {
            // create a new grid element for each year
            var year_grid = document.createElement("div");
            year_grid.classList.add("grid");
            year_grid.classList.add("flow-vert");

            // create our year header
            var year_element = document.createElement("div");
            year_element.classList.add("cell");
            year_element.classList.add("year-header");
            year_element.innerText = year;
            year_grid.appendChild(year_element);

            // generate months
            for (var month = 0; month < 12; ++ month)
            {
                // create a new cell and grid for our month
                var month_wrapper = document.createElement("div");
                month_wrapper.classList.add("cell");
                month_wrapper.classList.add("month-divider");
                month_wrapper.classList.add("month-bg");
                month_wrapper.classList.add("centred");

                var month_grid = document.createElement("div");
                month_grid.classList.add("grid");
                month_grid.classList.add("flow-vert");

                // create our month title
                var month_element = document.createElement("div");
                month_element.classList.add("cell");
                month_element.classList.add("month-header");
                month_element.innerText = month_names[month];
                month_grid.appendChild(month_element);

                // calculate how many days are in this month
                var day_count = days_in_month(month+1, year);

                // generate days
                for (var day = 1; day <= day_count; ++ day)
                {
                    // create days in a 7x1 format (col, row)
                    if (((day - 1) % 7) == 0)
                    {
                        // create an element wrapper
                        var w = document.createElement("div");
                        w.classList.add("cell");

                        // create a new grid for our weeks
                        var week_wrapper = document.createElement("div");
                        week_wrapper.classList.add("grid");
                        week_wrapper.classList.add("flow-hor");

                        // update our circuit
                        w.appendChild(week_wrapper);
                        month_grid.appendChild(w);
                    }

                    // insert days into our current target wrapper
                    var day_element = document.createElement("div");
                    day_element.classList.add("cell");

                    // format our day string, so that (d < 0) would be 0X
                    day_element.innerText = (day < 10 ? `0${day}` : day);

                    // if this day is our current date, add a marker to it
                    if ((month == date.getMonth() &&
                        (day == date.getDate()) &&
                        (year == (1900 + date.getYear()))))
                    {
                        day_element.setAttribute("id", "today");
                        day_element.classList.add("today");
                    }

                    week_wrapper.appendChild(day_element);
                }

                // update our node circuit
                month_wrapper.appendChild(month_grid);
                year_grid.appendChild(month_wrapper);
            }

            calendar.appendChild(year_grid);
        }

        // insert our generated calendar to the calendar wrapper node
        calwrap.appendChild(calendar);

        // update our generation status
        cal_generated = true;
    };

    // handle today view focus
    document.getElementById("todayBtn").onclick = function(e)
    {
        // check if we have generated a calendar yet
        if (cal_generated)
        {
            // check if the "today" item exists in our calendar
            if (document.getElementById("today"))
            {
                // get its reference
                var todayref = document.getElementById("today");

                // scroll to it
                var position = todayref.getBoundingClientRect();
                var speed = 256;
                animated_scroll(window.scrollY,
                                window.scrollY + position.y - 256,
                                (position.y > 0 ? speed : -speed));

                console.log(position.y)
            }
            else
            {
                show_message("Error", "Your calendar's range does not include today's date.");
            }
        }
        else
        {
            // show error
            show_message("Error", "You must create a calendar first!");
        }
    };

    // handle message box dismissal
    document.getElementById("dismiss").onclick = hide_message;
    overlay.onclick = hide_message;

    // hide our message box
    hide_message();
};

using extension auth;

module default {

    type User{
        required email: str{
            constraint regexp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
        };
        required first_name: str;
        required last_name: str;
        required frequency: Frequency;
        required password: str;
        required data_joined: cal::local_datetime{
            readonly := true;
        };

        constraint exclusive on ((.email, .frequency));
        # constraint max_len_value(25) on ((.last_name, .first_name));
        # constraint min_len_value(3) on ((.last_name, .first_name));
    };

    type Frequency{
        frequency_type: str{
            constraint one_of("daily", "weekly", "monthly");
            default := "daily"
        };
        delivery_day: str{
            constraint one_of("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday");
            default := "monday"
        };
        delivery_time: str{
            constraint one_of("morning", "noon", "night");
            default := "morning";
        };
        monthly_delivery_frequency: int16{
            constraint max_value(4);
            default := 1;
        };
        
    };
}

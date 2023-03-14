@dentist.post("/<int:id>/booking")
@jwt_required()
@user_authentication
def make_appointment(user,id):
    try:  
        booking_fields = booking_schema.load(request.json)
        dentist = Dentist.query.filter_by(id=id).first()
        #check if the dentist is exist or not
        if not dentist:
            return abort(404, description="dentist not exist")
        
        #if user already has a booking with "Open" status in the system, he/she can not book again unless delete that one first
        exist = Booking.query.filter_by(user_id=user.id, status="Open").first()
        if exist:
            return abort(409, description="You already have an open booking in the system. Before booking a new one, please ensure to cancel any existing booking in the system.")


        data = Booking.query.filter_by(dentist_id=id, date=booking_fields["date"])
        #check the booking date, if it exists, then check the time
        if data:
            #check each booked time in system with the json "time", if it's less than 30min, this time is not available
            for book in data:
                t1 = datetime.strptime(str(book.time), '%H:%M:%S')
                try: 
                    t2 = datetime.strptime(booking_fields["time"], '%H:%M:%S')
                except ValueError:
                    return abort(400, description="Invalid time format. Please use HH:MM:SS format.")
                #check the difference between those two time. 1800 second equal to 30min
                delta = t1 - t2
                sec = delta.total_seconds()
                if abs(sec) < 1800:
                    return abort(409, description="This time period is already book out, please selete another time")

        booking = Booking()
        booking.date = booking_fields["date"]
        booking.time = booking_fields["time"]
        # if "status" in booking_fields:
        #     booking.status = booking_fields["status"]
        booking.user_id = user.id
        booking.dentist_id = id
        db.session.add(booking)
        db.session.commit()

        return jsonify(booking_schema.dump(booking))
    except ValidationError as e:
        return abort(401, description = e.messages)
    # return an error if some of the compulsory field are missing
    except KeyError as e:
        return abort(401, description = f"{e.args} is missing" )
    
how to fix this code and handle the dataerror when user input wrong format of date
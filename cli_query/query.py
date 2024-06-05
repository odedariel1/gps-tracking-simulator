import server.bll as bll

device = input("enter device id:")

device_data = bll.json_reader(f"../data/{device}.json")

if len(device_data) == 0:
    print("device doesnt exist")
else:
    data_list = bll.show_all_point_from_last_minute(device)
    if data_list:
        for data in data_list:
            print(data)
            print(f"distance from start: {bll.distance_from_start(data)}")
        print(f"same latitude points: {bll.count_same_latitude(device)}")
        print(f"total routh: {bll.calc_routh(device)}")
    else:
        print("no data from the last minute")

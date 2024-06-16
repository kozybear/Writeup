## Days 3
## Challenge : Meerkat 
## Cat : SOC
- Level : Easy 
- Link: https://app.hackthebox.com/sherlocks/Meerkat
- Scenario :

  As a fast-growing startup, Forela has been utilising a business management platform. Unfortunately, our documentation is scarce, and our administrators aren't the most security aware. As our new security provider we'd like you to have a look at some PCAP and log data we have exported to confirm if we have (or have not) been compromised.

## Solving :

### Q1 : We believe our Business Management Platform server has been compromised. Please can you confirm the name of the application running?
- Firstly, i check Statistics -> Endpoint. I see some IP addresses with larger than normal number of packets: ```156.146.62.213,54.144.148.213,34.207.150.13,172.31.6.44``` . Especially the fourth address, I continued to check in the TCP section. The number of packets sent to the following 3 ports is the largest: ```61254,37022,8080```. Filter by keyword: ```ip.addr == 172.31.6.44 && tcp.port == [port number]```.The first two ports have some information, but it doesn't help me answer question number 1. But on port 8080, we can see some streams recording the following information:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/6c5bfe5f-0425-48dc-b315-cb75500a5320)

- Try searching for Bonita Application and we can see it is Bonitasoft :

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/dc459573-e0b0-4e0f-a2a9-326a3407154e)

-> *Answer : Bonitasoft*

### Q2 : We believe the attacker may have used a subset of the brute forcing attack category - what is the name of the attack carried out?
- Check some streams containing POST /bonita/... . We can see the information including: username and password . Filter by keyword: ```http contains "username"``` :

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/cfc440f0-f5e2-49d5-b28f-efb99f187dfd)

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/6a6dc4be-7e81-4895-935f-94e1ba62d5fa)

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/3088c322-4be5-4b11-9c93-9d10f5d85d68)

- After filtered, you can see their number is very large. From that we can deduce that this is a bruteforce attack. Search MITRE attack bruteforce, there are 4 types, but ending with the letter f, there is only ```Credential Stuffing```.

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/2c3b2a15-75a0-4314-992a-97cf28140407)

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/7e784ae4-c1bc-4ad0-971e-a7cca76dbfb4)

-> *Answer: Credential Stuffing*

### Q3 : Does the vulnerability exploited have a CVE assigned - and if so, which one?

- Check JSON file, we can got answer for it :

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/c1bfca22-8ae8-4e93-a8f3-977394838250)

-> *Answer : CVE-2022-25237*

### Q4 : Which string was appended to the API URL path to bypass the authorization filter by the attacker's exploit?

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/a6d2ca36-4655-483f-b2e2-dafa9faff59d)

-> *Answer : i18ntranslation*

### Q5 : How many combinations of usernames and passwords were used in the credential stuffing attack?
- Filter by keyword : ```http contains "username"``` .

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/a533e427-4cc0-4476-99e3-02e6a0c804c8)

- Because i'm too lazy to count it, I used Tshark and Python to do it:

  ```tshark
  tshark -r meerkat.pcap -Y 'http contains "username"' -T fields -e http.request.full_uri -e http.file_data -e tcp.stream > out.txt
  ```
- and Python :
  ```python
  # Read the extracted streams from the file
  with open('out2.txt', 'r') as file:
      lines = file.readlines()
  
  streams = {}
  unique_data_set = set()  # Set to track unique data entries
  
  for line in lines:
      parts = line.strip().split('\t')
      if len(parts) >= 3:
          uri, data, stream = parts
          if stream not in streams:
              streams[stream] = {
                  'uri': uri,
                  'data': set()  # Use a set to track unique data within a stream
              }
          streams[stream]['data'].add(data)
  
  # Count the number of unique streams
  unique_stream_count = len(streams)
  
  # Print out the streams and their associated data
  for stream, details in streams.items():
      print(f"Stream {stream}:")
      print(f"URI: {details['uri']}")
      for data in details['data']:
          if data not in unique_data_set:
              print(f"Data: {data}")
              unique_data_set.add(data)
      print("\n")
  
  # Print the count of unique streams
  print(f"Number of unique streams containing 'username': {unique_stream_count}")
  ```

  - We get the result 59, but it is not correct. I noticed the last 3 lines have no data, so I removed 3 and it is correct.

   ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/828ec468-cac1-499b-9786-df3223d19249)

-> *Answer : 56*

### Q6 : Which username and password combination was successful?

- Filter ```http.response.code >= 200 && http.response.code <= 300``` . To understand more about them, you can read the following document: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/2e077104-62be-4f90-a8ca-a89554cccf39)

- Check and pay special attention to the code 204 - loginservice. We can see the information we are looking for here. Or simply filter http and pay attention to the flow when the attacker starts bypassing:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/9fb02b52-6262-4fbb-9f7c-cb1a9883387a)

-> *Answer : seb.broom@forela.co.uk:g0vernm3nt*

### Q7 : If any, which text sharing site did the attacker utilise?
- Filtering by http, we can see the following line:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/7ae12a9f-bb5c-4c53-85d0-197ed9bee2cb)

-> *Answer : pastes.io*
### Q8 : Please provide the filename of the public key used by the attacker to gain persistence on our host.

- Check the file list in File -> Export Objects -> HTTP. You can see the name of the file from pastes.io that we found:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/795d2d22-99bd-4d55-8f71-152b8f88a7d6)

- I tried submitting the file name but it was incorrect. I tried downloading the file again, but it gave me a 403 error. I thought it was expired so I tried using the Wayback Machine and found the result here:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/eb616d03-5ea7-4a45-aced-d663bcff83b7)

-> *Answer : hffgra4unv*
### Q9 : Can you confirmed the file modified by the attacker to gain persistence?
- The answer is also in the file we just found in question 8:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/63d21fa9-c68f-4667-a26c-1534d80a2867)

-> *Answer : /home/ubuntu/.ssh/authorized_keys*
### Q10 : Can you confirm the MITRE technique ID of this type of persistence mechanism?

- From the answer to question 9, we can search it on GG and get the result:

  ![image](https://github.com/cozy404/WriteupsFreeTime/assets/130491266/23374e24-fa45-4c68-9041-60c3b790668f)

-> *Answer : T1098.004*


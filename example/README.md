# Sample Queries

from Nexmark


## Usage

`mvn clean package`


## Queries

see https://github.com/pentium3/sys_reading/issues/73#issuecomment-930817091

### Query1: map + filter + sink

Input parameter: event generating rate.  ```[<rate> <duration> ]^n```

### Query3: a stateful record-at-a-time two-input operator (incremental join) 

contains 2 sources: auctions and persons

![image](https://user-images.githubusercontent.com/7352163/144359118-dd0fd056-d270-4c54-b8fc-40adba3539c7.png)

Input parameter: event generating rate.  ```[<auctions_rate> <duration> <persons_rate> <duration> ]^n```

### Query5: sliding window

![image](https://user-images.githubusercontent.com/7352163/144932007-2109feff-f978-4b04-a811-08ccb121547c.png)

Input parameter: event generating rate.  ```[<rate> <duration> ]^n```

### Query8: tumbling window join

![image](https://user-images.githubusercontent.com/7352163/144933551-a0582476-9cbd-410c-8265-4b0e9d6946d3.png)

Input parameter: event generating rate.  ```[<auctions_rate> <duration> <persons_rate> <duration> ]^n```




# Architecture Notes

```
+----------------------+      +-----------------+      +-----------------------+
|  config_parser.py    | ---> | topology_builder| ---> | validator.py          |
+----------------------+      +-----------------+      +-----------------------+
             \                                            /           \
              \                                          /             \
               v                                        v               v
          +-----------------+                   +---------------+   +-----------+
          |   optimizer.py  |                   | simulator.py  |   |  main.py |
          +-----------------+                   +---------------+   +-----------+
```

- Threads per device with a simple IPC bus (queue). 
- Outputs written under `outputs/` for easy grading.

#!bin/bash
docker run -d -p 8888:8888 -v ~/Dropbox/_SPACE/_NOTEBOOKS/:/home/jovyan/work -e PASSWORD="kristiyanto" --restart=always -p 4040:4040 -p 4041:4041 -e GRANT_SUDO=yes jupyter/all-spark-notebook

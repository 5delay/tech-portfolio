for url in "pr" "opinion" "supplier" "performance" "renovation" "rebranding" "reopening" "viewpoint" "casestudy" "yearbook" "view-with-article" "report" "whitepaper"
do
    python ./hospitalitynet.py -u ${url} -s csv
done
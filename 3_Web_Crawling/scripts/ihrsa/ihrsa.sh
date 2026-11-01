for url in "member-retention" "fitness-programming" "staffing" "equipment" "leadership" "personal-training" "facilities" "wellness-community-programming" "sales-marketing" "strategy-finance" "legal" "technology" "coronavirus" 
do 
    python ./ihrsa.py -u ${url} -s csv
done

for url in "industry-news"
do 
    python ./ihrsa_industry.py -u ${url} -s csv
done
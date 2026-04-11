#!/usr/bin/env python3
"""Generate rankings.js from GSC data embedded below."""
import json, re

# Page + Country data (from GSC)
PAGE_COUNTRY_RAW = """
https://www.vantagecircle.com/en/blog/self-apprais|ind|69|6406|1.1|9.9
https://www.vantagecircle.com/en/blog/retirement-g|ind|66|4431|1.5|14.1
https://www.vantagecircle.com/en/blog/administrati|usa|50|4140|1.2|15.5
https://www.vantagecircle.com/en/blog/maxwells-5-l|usa|50|5555|0.9|7.8
https://www.vantagecircle.com/en/blog/april-employ|usa|41|2123|1.9|8.9
https://www.vantagecircle.com/en/blog/companies-wi|usa|41|8563|0.5|28.1
https://www.vantagecircle.com/en/blog/eid-gifts-fo|ind|29|293729|0.0|1.0
https://www.vantagecircle.com/en/blog/superlative-|usa|24|1046|2.3|10.5
https://www.vantagecircle.com/en/blog/employee-awa|ind|20|1910|1.0|11.3
https://www.vantagecircle.com/en/blog/samples-appr|ind|17|808|2.1|16.4
https://www.vantagecircle.com/en/blog/icebreaker-q|usa|17|7399|0.2|44.8
https://www.vantagecircle.com/en/blog/maxwells-5-l|phl|17|542|3.1|3.4
https://www.vantagecircle.com/en/blog/appreciation|ind|16|813|2.0|11.7
https://www.vantagecircle.com/en/blog/appraisal-co|ind|15|1391|1.1|15.8
https://www.vantagecircle.com/en/blog/zoom-icebrea|usa|15|21275|0.1|12.6
https://www.vantagecircle.com/en/blog/maxwells-5-l|ind|13|1189|1.1|4.4
https://www.vantagecircle.com/en/blog/employee-awa|usa|11|9306|0.1|26.0
https://www.vantagecircle.com/en/blog/gift-card-in|usa|11|774|1.4|54.6
https://www.vantagecircle.com/en/blog/compliments-|ind|10|501|2.0|9.6
https://www.vantagecircle.com/en/blog/compliments-|usa|10|2211|0.5|18.8
https://www.vantagecircle.com/en/blog/employee-awa|phl|10|3309|0.3|9.4
https://www.vantagecircle.com/en/blog/maxwells-5-l|can|10|491|2.0|8.4
https://www.vantagecircle.com/en/blog/maxwells-5-l|gbr|10|898|1.1|17.6
https://www.vantagecircle.com/en/blog/amazing-chri|usa|10|47814|0.0|13.1
https://www.vantagecircle.com/en/blog/differentiat|ind|8|301|2.7|14.8
https://www.vantagecircle.com/en/blog/maxwells-5-l|sgp|8|206|3.9|4.0
https://www.vantagecircle.com/en/blog/social-recog|ind|8|85|9.4|10.3
https://www.vantagecircle.com/en/blog/contemporary|nzl|8|119|6.7|14.0
https://www.vantagecircle.com/en/blog/administrati|can|7|425|1.6|10.0
https://www.vantagecircle.com/en/blog/compliments-|can|7|165|4.2|21.3
https://www.vantagecircle.com/en/blog/eid-gifts-fo|usa|7|254|2.8|23.1
https://www.vantagecircle.com/en/blog/ice-breaker-|usa|6|9107|0.1|39.5
https://www.vantagecircle.com/en/blog/office-decor|ind|6|474|1.3|33.9
https://www.vantagecircle.com/en/blog/womens-histo|phl|6|388|1.5|9.7
https://www.vantagecircle.com/en/blog/words-of-app|ind|6|1344|0.4|14.8
https://www.vantagecircle.com/en/blog/employee-eng|usa|6|1208|0.5|14.1
https://www.vantagecircle.com/en/blog/april-employ|ind|6|125|4.8|10.3
https://www.vantagecircle.com/en/blog/eid-gifts-fo|gbr|5|275|1.8|7.6
https://www.vantagecircle.com/en/blog/gift-card-in|can|5|16|31.2|24.0
https://www.vantagecircle.com/en/blog/importance-o|ind|5|73|6.8|9.2
https://www.vantagecircle.com/en/blog/maxwells-5-l|aus|5|259|1.9|9.6
https://www.vantagecircle.com/en/blog/maxwells-5-l|nga|5|249|2.0|3.4
https://www.vantagecircle.com/en/blog/retirement-g|usa|5|2461|0.2|47.8
https://www.vantagecircle.com/en/blog/retirement-g|zaf|5|155|3.2|19.7
https://www.vantagecircle.com/en/blog/self-apprais|mys|5|190|2.6|8.4
https://www.vantagecircle.com/en/blog/diversity-an|ind|5|866|0.6|24.7
https://www.vantagecircle.com/en/blog/employee-eng|ind|5|227|2.2|25.3
https://www.vantagecircle.com/en/blog/team-buildin|ind|4|2689|0.1|36.1
https://www.vantagecircle.com/en/blog/team-buildin|usa|4|30490|0.0|51.4
https://www.vantagecircle.com/en/blog/employee-rec|usa|4|2334|0.2|19.1
https://www.vantagecircle.com/en/blog/easter-gifts|usa|4|597|0.7|10.9
https://www.vantagecircle.com/en/blog/contemporary|aus|4|110|3.6|11.8
https://www.vantagecircle.com/en/blog/appraisal-co|hkg|4|134|3.0|26.5
https://www.vantagecircle.com/en/blog/reinforcemen|ind|4|72|5.6|19.8
https://www.vantagecircle.com/en/blog/rewards-and-|ind|4|2372|0.2|16.9
https://www.vantagecircle.com/en/blog/dei-calendar|usa|3|5693|0.1|38.8
https://www.vantagecircle.com/en/blog/employee-cli|usa|3|298|1.0|17.4
https://www.vantagecircle.com/en/blog/employee-pul|ind|3|184|1.6|17.7
https://www.vantagecircle.com/en/blog/employee-pro|ind|3|177|1.7|13.9
https://www.vantagecircle.com/en/blog/hr-calendar/|usa|3|13555|0.0|6.3
https://www.vantagecircle.com/en/blog/icebreaker-q|gbr|3|1745|0.2|43.5
https://www.vantagecircle.com/en/blog/nepotism-in-|usa|3|10743|0.0|7.2
https://www.vantagecircle.com/en/blog/office-prank|usa|3|368|0.8|46.3
https://www.vantagecircle.com/en/blog/self-apprais|usa|3|4634|0.1|53.7
https://www.vantagecircle.com/en/blog/teamwork-and|ind|3|3615|0.1|10.0
https://www.vantagecircle.com/en/blog/womens-safet|ind|3|180|1.7|11.2
https://www.vantagecircle.com/en/blog/celebrating-|usa|3|40|7.5|19.2
https://www.vantagecircle.com/en/blog/companies-wi|gbr|3|1180|0.3|48.4
https://www.vantagecircle.com/en/blog/contingency-|ind|3|2456|0.1|7.5
https://www.vantagecircle.com/en/blog/holi-celebra|usa|3|45|6.7|27.6
https://www.vantagecircle.com/en/blog/modern-metho|ind|3|230|1.3|22.7
https://www.vantagecircle.com/en/blog/spot-award/|ind|3|864|0.3|7.1
https://www.vantagecircle.com/en/blog/workplace-ha|ind|3|24|12.5|36.9
https://www.vantagecircle.com/en/blog/contemporary|usa|3|987|0.3|17.7
https://www.vantagecircle.com/en/blog/employee-rec|usa|3|309|1.0|9.7
https://www.vantagecircle.com/en/blog/employee-eng|ind|2|318|0.6|10.7
https://www.vantagecircle.com/en/blog/employee-rec|usa|2|414|0.2|34.3
https://www.vantagecircle.com/en/blog/types-of-div|gbr|2|298|0.7|22.7
https://www.vantagecircle.com/en/blog/employee-rec|gbr|2|944|0.2|31.5
https://www.vantagecircle.com/en/blog/employee-rec|ind|2|425|0.5|19.6
https://www.vantagecircle.com/en/blog/employee-rew|ind|2|53949|0.0|4.5
https://www.vantagecircle.com/en/blog/employee-sat|ind|2|231|0.9|33.1
https://www.vantagecircle.com/en/blog/employee-spo|ind|2|199|1.0|6.7
https://www.vantagecircle.com/en/blog/fun-games-in|ind|2|615|0.3|28.7
https://www.vantagecircle.com/en/blog/gift-card-in|ind|2|132|1.5|26.7
https://www.vantagecircle.com/en/blog/handle-emplo|ind|2|513|0.4|11.0
https://www.vantagecircle.com/en/blog/hr-calendar/|ind|2|310|0.6|11.1
https://www.vantagecircle.com/en/blog/ice-breaker-|ind|2|1480|0.1|11.0
https://www.vantagecircle.com/en/blog/diversity-an|ind|2|52|3.8|12.0
https://www.vantagecircle.com/en/blog/year-end-rec|usa|2|195537|0.0|10.5
https://www.vantagecircle.com/en/blog/zoom-icebrea|can|2|80|2.5|33.0
https://www.vantagecircle.com/en/blog/employee-bon|ind|2|342|0.6|13.5
https://www.vantagecircle.com/en/blog/best-hrms-so|ind|2|3822|0.1|28.8
https://www.vantagecircle.com/en/blog/blue-collar-|usa|2|3560|0.1|10.7
https://www.vantagecircle.com/en/blog/compensation|usa|2|2834|0.1|19.7
https://www.vantagecircle.com/en/blog/employee-onb|ind|2|36841|0.0|8.8
https://www.vantagecircle.com/en/blog/self-apprais|gbr|2|1165|0.2|45.5
https://www.vantagecircle.com/en/blog/leadership-b|usa|2|335|0.6|25.2
https://www.vantagecircle.com/en/blog/employee-eng|usa|1|6172|0.0|66.9
https://www.vantagecircle.com/en/blog/employee-ben|usa|1|2691|0.0|53.6
https://www.vantagecircle.com/en/blog/employee-mor|usa|1|3378|0.0|42.4
https://www.vantagecircle.com/en/blog/employee-sho|usa|1|3257|0.0|4.1
https://www.vantagecircle.com/en/blog/employee-ret|ind|1|299|0.3|60.8
https://www.vantagecircle.com/en/blog/employee-spo|usa|1|1718|0.1|10.0
https://www.vantagecircle.com/en/blog/amazon-leade|usa|1|2000|0.1|5.8
https://www.vantagecircle.com/en/blog/employee-app|usa|1|11912|0.0|12.8
https://www.vantagecircle.com/en/blog/exit-intervi|usa|1|1062|0.1|66.1
https://www.vantagecircle.com/en/blog/inclusion-at|usa|1|15389|0.0|11.0
https://www.vantagecircle.com/en/blog/intrinsic-re|usa|1|1326|0.1|13.9
https://www.vantagecircle.com/en/blog/extrinsic-re|usa|1|1035|0.1|14.9
https://www.vantagecircle.com/en/blog/employee-rel|usa|1|906|0.1|58.5
https://www.vantagecircle.com/en/blog/employee-inv|gbr|1|309|0.3|57.6
https://www.vantagecircle.com/en/blog/career-miles|ind|1|1370|0.1|8.0
https://www.vantagecircle.com/en/blog/employee-eng|can|1|108|0.9|27.9
https://www.vantagecircle.com/en/blog/contingency-|phl|2|1270|0.2|9.1
https://www.vantagecircle.com/en/blog/employee-eng|ind|1|47|2.1|29.5
https://www.vantagecircle.com/en/blog/employee-dis|ind|1|145|0.7|18.1
https://www.vantagecircle.com/en/blog/employee-per|ind|1|90|1.1|49.6
https://www.vantagecircle.com/en/blog/hr-analytics|ind|1|372|0.3|49.7
https://www.vantagecircle.com/en/blog/incentive-th|ind|1|478|0.2|10.9
https://www.vantagecircle.com/en/blog/employee-dev|usa|1|3895|0.0|16.8
https://www.vantagecircle.com/en/blog/communicatio|usa|1|624|0.2|49.5
https://www.vantagecircle.com/en/blog/employee-rec|ind|1|270|0.4|10.8
https://www.vantagecircle.com/en/blog/st-patricks-|usa|2|526|0.4|38.6
https://www.vantagecircle.com/en/blog/memorial-day|usa|2|195|1.0|19.4
https://www.vantagecircle.com/en/blog/employee-eng|usa|1|6172|0.0|66.9
https://www.vantagecircle.com/en/blog/employee-eng|ind|2|318|0.6|10.7
https://www.vantagecircle.com/en/blog/effective-fe|ind|1|759|0.1|3.8
"""

# Top pages data (overall, from get_top_pages)
TOP_PAGES = [
    {"p":"/en/blog/employee-award-titles/","c":361,"i":44424,"ctr":0.8,"pos":15.1},
    {"p":"/en/blog/self-appraisal-comments/","c":331,"i":43253,"ctr":0.8,"pos":17.8},
    {"p":"/en/blog/april-employee-engagement-ideas/","c":236,"i":9139,"ctr":2.6,"pos":7.0},
    {"p":"/en/blog/maxwells-5-levels-of-leadership/","c":235,"i":21083,"ctr":1.1,"pos":6.7},
    {"p":"/en/blog/retirement-gift/","c":206,"i":17096,"ctr":1.2,"pos":23.0},
    {"p":"/en/blog/companies-with-best-employee-perks/","c":175,"i":26430,"ctr":0.7,"pos":18.6},
    {"p":"/en/blog/appraisal-comments/","c":162,"i":21546,"ctr":0.8,"pos":31.9},
    {"p":"/en/blog/appreciation-mail-to-team/","c":162,"i":17370,"ctr":0.9,"pos":12.3},
    {"p":"/en/blog/compliments-for-coworkers/","c":140,"i":15089,"ctr":0.9,"pos":11.3},
    {"p":"/en/blog/eid-gifts-for-coworkers/","c":139,"i":299596,"ctr":0.0,"pos":1.1},
    {"p":"/en/blog/administrative-professionals-day-gif","c":133,"i":9376,"ctr":1.4,"pos":14.4},
    {"p":"/en/blog/employee-engagement-committee-names/","c":98,"i":5864,"ctr":1.7,"pos":8.7},
    {"p":"/en/blog/samples-appreciation-letters-to-empl","c":96,"i":11669,"ctr":0.8,"pos":21.5},
    {"p":"/en/blog/superlative-awards-for-work/","c":85,"i":3078,"ctr":2.8,"pos":9.1},
    {"p":"/en/blog/words-of-appreciation-for-employees/","c":67,"i":15368,"ctr":0.4,"pos":28.2},
    {"p":"/en/blog/icebreaker-questions/","c":56,"i":13382,"ctr":0.4,"pos":41.3},
    {"p":"/en/blog/contemporary-leadership/","c":47,"i":3849,"ctr":1.2,"pos":13.9},
    {"p":"/en/blog/ice-breaker-games-for-work/","c":45,"i":33839,"ctr":0.1,"pos":34.2},
    {"p":"/en/blog/team-building-activities-for-work/","c":42,"i":92975,"ctr":0.0,"pos":53.3},
    {"p":"/en/blog/hr-calendar/","c":41,"i":48482,"ctr":0.1,"pos":4.0},
    {"p":"/en/blog/gift-card-incentives-for-employees/","c":37,"i":2030,"ctr":1.8,"pos":46.5},
    {"p":"/en/blog/zoom-icebreakers/","c":34,"i":27192,"ctr":0.1,"pos":13.6},
    {"p":"/en/blog/easter-gifts-for-employees/","c":32,"i":2606,"ctr":1.2,"pos":9.8},
    {"p":"/en/blog/fun-games-in-office/","c":31,"i":8007,"ctr":0.4,"pos":36.1},
    {"p":"/en/blog/csr-activities-to-boost-employee-eng","c":29,"i":9832,"ctr":0.3,"pos":51.1},
    {"p":"/en/blog/employee-engagement-trends/","c":21,"i":4248,"ctr":0.5,"pos":22.9},
    {"p":"/en/blog/differentiation-strategy/","c":20,"i":4499,"ctr":0.4,"pos":44.0},
    {"p":"/en/blog/employee-pulse-survey-questions/","c":19,"i":3509,"ctr":0.5,"pos":39.2},
    {"p":"/en/blog/womens-safety-workplace/","c":17,"i":1278,"ctr":1.3,"pos":17.8},
    {"p":"/en/blog/womens-history-month-ideas/","c":16,"i":1928,"ctr":0.8,"pos":22.5},
    {"p":"/en/blog/office-decor-ideas/","c":15,"i":6895,"ctr":0.2,"pos":40.0},
    {"p":"/en/blog/employee-climate-survey/","c":14,"i":938,"ctr":1.5,"pos":13.5},
    {"p":"/en/blog/years-of-service-award/","c":14,"i":6636,"ctr":0.2,"pos":29.6},
    {"p":"/en/blog/celebrating-ramadan-at-work/","c":13,"i":522,"ctr":2.5,"pos":10.8},
    {"p":"/en/blog/employee-performance-survey/","c":13,"i":2835,"ctr":0.5,"pos":63.4},
    {"p":"/en/blog/sample-survey-questions-for-sales-te","c":13,"i":1217,"ctr":1.1,"pos":19.6},
    {"p":"/en/blog/amazing-christmas-gifts-for-employee","c":12,"i":67190,"ctr":0.0,"pos":18.9},
    {"p":"/en/blog/diversity-and-inclusion-trends/","c":12,"i":1860,"ctr":0.6,"pos":22.9},
    {"p":"/en/blog/diversity-and-inclusion/","c":12,"i":8435,"ctr":0.1,"pos":51.7},
    {"p":"/en/blog/employee-behaviors/","c":12,"i":3158,"ctr":0.4,"pos":28.7},
    {"p":"/en/blog/employee-relationship-management/","c":12,"i":3010,"ctr":0.4,"pos":57.7},
    {"p":"/en/blog/podcasts/","c":12,"i":967,"ctr":1.2,"pos":5.5},
    {"p":"/en/blog/best-hrms-softwares/","c":11,"i":18590,"ctr":0.1,"pos":42.7},
    {"p":"/en/blog/employee-engagement-calendar/","c":11,"i":15293,"ctr":0.1,"pos":5.8},
    {"p":"/en/blog/employee-recognition-board/","c":11,"i":5633,"ctr":0.2,"pos":17.1},
    {"p":"/en/blog/social-recognition/","c":11,"i":1025,"ctr":1.1,"pos":21.3},
    {"p":"/en/blog/types-of-meetings/","c":11,"i":1860,"ctr":0.6,"pos":27.7},
    {"p":"/en/blog/employee-shout-outs/","c":22,"i":6268,"ctr":0.4,"pos":6.2},
    {"p":"/en/blog/types-of-diversity/","c":22,"i":26367,"ctr":0.1,"pos":5.8},
    {"p":"/en/blog/activities-diversity-and-inclusion/","c":24,"i":8231,"ctr":0.3,"pos":45.8},
    {"p":"/en/blog/catchy-employee-engagement-survey-na","c":24,"i":2395,"ctr":1.0,"pos":4.3},
    {"p":"/en/blog/contingency-leadership/","c":25,"i":18554,"ctr":0.1,"pos":13.9},
    {"p":"/en/blog/advantages-and-disadvantages-of-rewa","c":25,"i":2680,"ctr":0.9,"pos":36.6},
]

# Top keywords for US
KW_USA = [
    {"q":"april employee engagement ideas","c":21,"i":311,"ctr":6.8,"pos":7.5},
    {"q":"5 levels of leadership","c":7,"i":1059,"ctr":0.7,"pos":6.5},
    {"q":"companies with the best employee benefits","c":10,"i":64,"ctr":15.6,"pos":3.6},
    {"q":"administrative professionals day gift ideas","c":8,"i":259,"ctr":3.1,"pos":11.4},
    {"q":"employee engagement ideas for april","c":10,"i":160,"ctr":6.2,"pos":5.4},
    {"q":"john maxwell 5 levels of leadership","c":6,"i":290,"ctr":2.1,"pos":3.6},
    {"q":"work superlatives","c":7,"i":88,"ctr":8.0,"pos":9.0},
    {"q":"superlatives for work","c":6,"i":72,"ctr":8.3,"pos":7.3},
    {"q":"companies with best employee discounts","c":5,"i":36,"ctr":13.9,"pos":4.5},
    {"q":"companies with the best perks","c":5,"i":34,"ctr":14.7,"pos":3.8},
    {"q":"vantage circle gift card","c":11,"i":22,"ctr":50.0,"pos":1.0},
    {"q":"ice breaker questions for team meetings","c":3,"i":179,"ctr":1.7,"pos":23.1},
    {"q":"employee recognition board","c":3,"i":195,"ctr":1.5,"pos":8.0},
    {"q":"gifts for administrative professionals","c":6,"i":195,"ctr":3.1,"pos":9.5},
    {"q":"levels of leadership","c":4,"i":188,"ctr":2.1,"pos":5.0},
    {"q":"emotional resonance","c":4,"i":654,"ctr":0.6,"pos":7.0},
    {"q":"superlative ideas for work","c":3,"i":25,"ctr":12.0,"pos":6.5},
    {"q":"dei tip of the month","c":2,"i":28,"ctr":7.1,"pos":9.5},
    {"q":"ice breaker questions for work","c":2,"i":190,"ctr":1.1,"pos":22.6},
    {"q":"fun committee names","c":2,"i":17,"ctr":11.8,"pos":2.8},
    {"q":"blue collar industries","c":2,"i":56,"ctr":3.6,"pos":3.9},
    {"q":"employee appreciation day 2026","c":2,"i":120,"ctr":1.7,"pos":12.2},
    {"q":"fun days to celebrate at work 2026","c":2,"i":22,"ctr":9.1,"pos":8.6},
    {"q":"admin day gifts","c":2,"i":91,"ctr":2.2,"pos":12.9},
    {"q":"memorial day celebration ideas for work","c":2,"i":13,"ctr":15.4,"pos":7.8},
    {"q":"names for employee engagement committee","c":2,"i":26,"ctr":7.7,"pos":14.5},
    {"q":"list of award categories for employees","c":2,"i":15,"ctr":13.3,"pos":13.5},
    {"q":"contemporary leaders","c":2,"i":46,"ctr":4.3,"pos":11.8},
    {"q":"leadership burnout","c":2,"i":150,"ctr":1.3,"pos":22.0},
    {"q":"ice breakers","c":2,"i":1212,"ctr":0.2,"pos":18.5},
]

# Top keywords for India
KW_IND = [
    {"q":"highlights of my performance during the year","c":23,"i":658,"ctr":3.5,"pos":4.0},
    {"q":"april employee engagement ideas","c":5,"i":37,"ctr":13.5,"pos":4.9},
    {"q":"appreciation mail to team","c":11,"i":47,"ctr":23.4,"pos":5.7},
    {"q":"compliments for coworkers","c":6,"i":8,"ctr":75.0,"pos":7.9},
    {"q":"social recognition","c":7,"i":30,"ctr":23.3,"pos":10.0},
    {"q":"creative award titles for employees","c":3,"i":71,"ctr":4.2,"pos":4.4},
    {"q":"list of award categories for employees","c":3,"i":71,"ctr":4.2,"pos":8.7},
    {"q":"self-appraisal comments by employee example","c":4,"i":203,"ctr":2.0,"pos":8.6},
    {"q":"appraisal comments by employee","c":2,"i":55,"ctr":3.6,"pos":4.4},
    {"q":"employee comments on appraisal","c":2,"i":163,"ctr":1.2,"pos":5.4},
    {"q":"differentiation strategy","c":3,"i":156,"ctr":1.9,"pos":11.6},
    {"q":"diversity and inclusion in the workplace","c":3,"i":151,"ctr":2.0,"pos":8.9},
    {"q":"appreciation letter for employee","c":3,"i":96,"ctr":3.1,"pos":6.8},
    {"q":"types of promotion in hrm","c":3,"i":87,"ctr":3.4,"pos":6.1},
    {"q":"women safety at workplace","c":3,"i":58,"ctr":5.2,"pos":7.7},
    {"q":"reinforcement theory in the workplace","c":4,"i":19,"ctr":21.1,"pos":16.9},
    {"q":"best retirement gifts for men","c":5,"i":255,"ctr":2.0,"pos":10.5},
    {"q":"endeavour meaning","c":6,"i":3370,"ctr":0.2,"pos":2.1},
    {"q":"endeavors meaning","c":5,"i":465,"ctr":1.1,"pos":2.0},
    {"q":"samples of appreciation letter","c":4,"i":5,"ctr":80.0,"pos":9.6},
    {"q":"appreciation message for good work","c":2,"i":134,"ctr":1.5,"pos":9.7},
    {"q":"team building and team work","c":2,"i":26,"ctr":7.7,"pos":4.4},
    {"q":"award title","c":2,"i":18,"ctr":11.1,"pos":3.9},
    {"q":"office beautification ideas","c":2,"i":8,"ctr":25.0,"pos":3.1},
    {"q":"importance of office communication","c":3,"i":16,"ctr":18.8,"pos":2.0},
    {"q":"promotion recommendation comments in appraisal","c":2,"i":63,"ctr":3.2,"pos":8.0},
    {"q":"recent trends in diversity management","c":2,"i":33,"ctr":6.1,"pos":3.2},
    {"q":"employee bonus","c":2,"i":60,"ctr":3.3,"pos":10.4},
    {"q":"employee engagement trends","c":2,"i":44,"ctr":4.5,"pos":11.3},
    {"q":"five levels of leadership","c":2,"i":17,"ctr":11.8,"pos":2.3},
]

# Parse page+country data
pages_by_country = {'usa': [], 'ind': []}
seen = set()
for line in PAGE_COUNTRY_RAW.strip().split('\n'):
    parts = line.split('|')
    if len(parts) != 6:
        continue
    url, country, clicks, impr, ctr, pos = parts
    url = url.strip()
    country = country.strip()
    if country not in ('usa', 'ind'):
        continue
    if '/en/blog/' not in url:
        continue
    # Extract slug from URL
    slug = url.replace('https://www.vantagecircle.com/en/blog/', '').rstrip('/')
    # Handle truncated URLs
    key = f"{slug}_{country}"
    if key in seen:
        continue
    seen.add(key)
    pages_by_country[country].append({
        'p': slug,
        'c': int(clicks.strip()),
        'i': int(impr.strip()),
        'ctr': float(ctr.strip()),
        'pos': float(pos.strip())
    })

# Sort by clicks desc
for country in pages_by_country:
    pages_by_country[country].sort(key=lambda x: -x['c'])

data = {
    'generated': '2026-04-11',
    'period': 'Last 28 days',
    'topPages': TOP_PAGES,
    'pages': pages_by_country,
    'keywords': {
        'usa': KW_USA,
        'ind': KW_IND
    }
}

js = 'const RANKINGS_DATA = ' + json.dumps(data, ensure_ascii=True) + ';'
output = '/Users/mrinmoyrabha/Desktop/aiclaude/content-writer-tracker/rankings.js'
with open(output, 'w') as f:
    f.write(js)

print(f'Generated rankings.js')
print(f'  Top pages: {len(TOP_PAGES)}')
print(f'  USA blog pages: {len(pages_by_country["usa"])}')
print(f'  India blog pages: {len(pages_by_country["ind"])}')
print(f'  USA keywords: {len(KW_USA)}')
print(f'  India keywords: {len(KW_IND)}')

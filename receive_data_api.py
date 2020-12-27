from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus


# Government OpenAPI Information: https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15043376
# Seoul City OpenAPI Information: http://data.seoul.go.kr/dataList/OA-20279/S/1/datasetView.do;jsessionid=EF730F0453C4F306BF7C15516BA71528.new_portal-svr-11

url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson"
queryParams = "?" + urlencode(
    {
        quote_plus("ServiceKey"): "서비스키",
        quote_plus("pageNo"): "1",
        quote_plus("numOfRows"): "10",
        quote_plus("startCreateDt"): "20200310",
        quote_plus("endCreateDt"): "20201226",
    }
)

request = Request(url + queryParams)
request.get_method = lambda: "GET"
response_body = urlopen(request).read()
print(response_body)


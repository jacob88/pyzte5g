from pyzte5g import ZTE_Client
from datetime import datetime


# result = requests.get(url='http://192.168.2.1/goform/goform_get_cmd_process?isTest=false&cmd=opms_wan_auto_mode%2Cdhcp_wan_status%2Cdatausage_remainamount%2Cdatausage_remaindays%2Cdatausage_remainrate%2Cdatausage_lowbalance%2Cdatausage_preactive%2Cdatausage_syncresult%2Cppp_status%2Cnew_version_state%2Cmdm_mcc%2Cmdm_mnc%2Cmsisdn_prepaid%2Csta_ip_status%2Cdatausage_prepaid%2Cmodem_main_state%2Cdm_showfotaicon%2Cdatausage_rechargesiteurl%2Cdatausage_plantype%2Cdatausage_allotedamount%2Cdatausage_usedamount%2Cdatausage_usedrate&multi_data=1', headers={'referer': 'http://192.168.2.1/index.html'})
# print(result.json())


# isTest=False, cmd='opms_wan_auto_mode,dhcp_wan_status,datausage_remainamount,datausage_remaindays,datausage_remainrate,datausage_lowbalance,datausage_preactive,datausage_syncresult,ppp_status,new_version_state,mdm_mcc,mdm_mnc,msisdn_prepaid,sta_ip_status,datausage_prepaid,modem_main_state,dm_showfotaicon,datausage_rechargesiteurl,datausage_plantype,datausage_allotedamount,datausage_usedamount,datausage_usedrate', multi_data=1


# var test_rd;
# $.ajax({
#     type: "GET",
#     url: "http://192.168.2.1/goform/goform_get_cmd_process?isTest=false&cmd=RD",
#     cache: false,
#     async: false,
#     error: function(e) {
#         test_rd = jQuery.parseJSON(e);
#     },
#     success: function(e) {
#         test_rd = jQuery.parseJSON(e);
#     }
# })
# var a = hex_md5(rd0 + rd1), u = test_rd.RD, d = hex_md5(a + u);
# var test_response;
# $.ajax({
#     type: "POST",
#     url: "http://192.168.2.1/goform/goform_set_cmd_process",
#     cache: false,
#     async: false,
#     data: {
#         isTest: false,
#         notCallback: true,
#         goformId: "DISCONNECT_NETWORK",
#         AD: d
#     },
#     error: function(e) {
#         test_response = jQuery.parseJSON(e);
#     },
#     success: function(e) {
#         test_response = jQuery.parseJSON(e);
#     }
# })
# console.log(test_response);


# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# import time
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options, executable_path='/home/jacob/src/pyzte5g/geckodriver')
# driver.get('http://192.168.2.1')

# url = 'http://192.168.2.1/goform/goform_set_cmd_process'
# goformId = 'LOGIN'
# password = 'cGFzc3dvcmQ='
# result = driver.execute_script(f"""
# var zte_modem_response;
# $.ajax({{
#     type: "POST",
#     url: "{url}",
#     cache: false,
#     async: false,
#     data: {{
#         isTest: false,
#         notCallback: true,
#         goformId: "{goformId}",
#         password: "{password}"
#     }},
#     error: function(data) {{
#         zte_modem_response = jQuery.parseJSON(data);
#     }},
#     success: function(e) {{
#         zte_modem_response = jQuery.parseJSON(e);
#     }}
# }});
# return zte_modem_response;
# """)

# time.sleep(3)

# result = driver.execute_script(f"""
# var test_rd;
# $.ajax({{
#     type: "GET",
#     url: "http://192.168.2.1/goform/goform_get_cmd_process?isTest=false&cmd=RD",
#     cache: false,
#     async: false,
#     error: function(e) {{
#         test_rd = jQuery.parseJSON(e);
#     }},
#     success: function(e) {{
#         test_rd = jQuery.parseJSON(e);
#     }}
# }});
# var a = hex_md5(rd0 + rd1), u = test_rd.RD, d = hex_md5(a + u);
# var test_response;
# $.ajax({{
#     type: "POST",
#     url: "http://192.168.2.1/goform/goform_set_cmd_process",
#     cache: false,
#     async: false,
#     data: {{
#         isTest: false,
#         notCallback: true,
#         goformId: "DISCONNECT_NETWORK",
#         AD: d
#     }},
#     error: function(e) {{
#         test_response = jQuery.parseJSON(e);
#     }},
#     success: function(e) {{
#         test_response = jQuery.parseJSON(e);
#     }}
# }});
# return test_response;
# """)

# driver.close()


test2 = ZTE_Client(url='http://192.168.2.1', password='password')
test2.connection.disconnect()

# result = test2.get_cmd_process(cmd=('realtime_tx_thrpt', 'realtime_rx_thrpt',))

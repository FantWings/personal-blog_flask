import json
from os import getenv
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models


class SMS:
    """腾讯云短信模块"""

    def __init__(
        self,
        SmsSdkAppId: str,
        TemplateId: str,
        SignName: str = '极点技术个人网',
    ):
        cred = credential.Credential(getenv("TENCENTCLOUD_SECRET_ID"), getenv("TENCENTCLOUD_SECRET_KEY"))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        self.client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
        self.req = models.SendSmsRequest()
        self.SmsSdkAppId = SmsSdkAppId
        self.SignName = SignName
        self.TemplateId = TemplateId

    def send(
        self,
        PhoneNumberSet: list,
        ParamSet: list,
    ):
        """
        TemplateId: 腾讯云模板ID
        ParamSet: 短信模板
        """

        params = {
            "PhoneNumberSet": PhoneNumberSet,
            "SmsSdkAppId": self.SmsSdkAppId,
            "SignName": self.SignName,
            "TemplateId": self.TemplateId,
            "TemplateParamSet": ParamSet
        }
        self.req.from_json_string(json.dumps(params))
        resp = self.client.SendSms(self.req)
        return resp.to_json_string()

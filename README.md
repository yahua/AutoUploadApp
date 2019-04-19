# AutoUploadApp
将ipa或者apk自动上传到pgyer或者fir

## 使用说明
1、可直接使用package文件下的uploadIpa可执行文件  （推荐使用）
2、自定义功能的话、可运行Upload_Ipa_Project工程

## upload.json说明
--不想编辑格式  可拷贝下来查看。。。

{
"uploadOpen":"1",   //肯定是1了， 由于从别的项目中剥离，保留了该字段，后期有时间再删除吧。。。
"uploadPlatform":"fir",  //上传平台
"ipaName":"ios.ipa",  同目录下上传app的文件名称
"uploadPlatformInfo":{
        "payer":{ //蒲公英平台
            "log":"测试payer自动打包上传",
            "uploadUrl":"https://www.pgyer.com/apiv2/app/upload",
            "_api_key":"xxxx",    //自己的apikey
            "buildInstallType":"2",  //应用安装方式，值为(1,2,3)。1：公开，2：密码安装，3：邀请安装。默认为1公开
            "buildPassword":"",
            "buildName":"appName",
            "ipa_version":"1.0.0"
        },
        "fir":{  //fir平台
            "log":"测试fir自动打包上传",
            "appsUrl":"http://api.fir.im/apps",
            "api_token":"",  //自己的apikey
            "bundle_id":"",
            "ipaName":"ipaName",
            "type":"ios",
            "ipa_build":"1.0.0",
            "ipa_version":"1.0.0"
        }
	},
"notifyToDingDing":"0",   //是否钉钉通知
"dingdingUrl":""  //钉钉机器人token地址 
}

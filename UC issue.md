
there is version issue

[Undetected Chrome Driver doesn't support Chrome 116 #297][#1]

[Add support for downloading Chromedriver versions 115+ #1478][#2]

[selenium.common.exceptions.WebDriverException:
Message: unknown error: cannot connect to chrome at 127.0.0.1:65490 from session not created: 
This version of ChromeDriver only supports Chrome version 114 
Current browser version is 116.0.5845.97][#3]

temp fix it [fix]
```commandline
pip install -e git+https://github.com/jdholtz/undetected-chromedriver.git@29551bd27954dacaf09864cf77935524db642c1b#egg=undetected_chromedriver
```

[#1]: https://github.com/charlesbel/Microsoft-Rewards-Farmer/issues/297
[#2]: https://github.com/ultrafunkamsterdam/undetected-chromedriver/pull/1478
[#3]: https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1477
[fix]: https://github.com/ultrafunkamsterdam/undetected-chromedriver/pull/1478#issuecomment-1680979672
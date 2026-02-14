# prompt.py

SPAM_CLASSIFY_PROMPT = """你是一个邮件分类系统。
请判断下面的邮件属于哪一类：
A. 正常邮件
B. 广告邮件
C. 诈骗邮件
示例：
邮件内容：双十一限时优惠，点击链接立刻领取优惠券。
答案：B
邮件内容：test smtp 198.23.254.212--
答案：B
邮件内容：smtp.linuxuser.site:25:0:127.0.0.1:1080:socks5:25
答案：B
邮件内容：gsudmswgebl iokijcsmg ykvhiy wocmydsmfa hsovovdq
答案：B
邮件内容：Have you received your funds valued $4,150,567.00 that was awarded to you by the NCIC.
答案：C
邮件内容：Your account has been compromised, please click the link to verify your information.
答案：C
邮件内容：会议时间调整为周三下午三点，请查收附件。
答案：A
邮件内容：项目进展已更新到文档，请大家查看。
答案：A
只输出一个大写字母，不要输出任何解释。
邮件内容：
{email}
"""

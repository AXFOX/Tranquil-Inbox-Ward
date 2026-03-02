# prompt.py

SPAM_CLASSIFY_PROMPT = """你是一个邮件分类系统。
请判断下面的邮件属于哪一类：
A. 正常邮件
B. 广告邮件
C. 诈骗邮件
示例：
邮件内容：双十一限时优惠，点击链接立刻领取优惠券。
答案：B
邮件内容：SMTP WORK !! 198.23.254.212
答案：B
邮件内容：test smtp 198.23.254.212--
答案：B
邮件内容：198.23.254.212 t_Smtp.LocalIP
答案：B
邮件内容：smtp.linuxuser.site:25:0:127.0.0.1:1080:socks5:25
答案：B
邮件内容：gsudmswgebl iokijcsmg ykvhiywocmydsmfahsovovdq
答案：B
邮件内容：Have you received your funds valued $4,150,567.00 that was awarded to you by the NCIC.
答案：C
邮件内容：Your account has been compromised, please click the link to verify your information.
答案：C
邮件内容：Dear Sir/Ma, How are you today?i am writing to you for an opportunity that will benefit us both immensely.I have discovered an abandoned overdue inheritance fund and I have made several attempts to locate any of my late client's extended relatives and this has proved unsuccessful. After several unsuccessful attempts to locate any member of his family, I contacted you and I am contacting you to assist in claiming & receiving the funds left behind by the late customer before they get confiscated or declared unclaimed. If you are interested in this transaction,kindly get back to me asap so that i can give the full details about this transaction. I urgently hope to get your response as soon as possible. Yours Sincerely, From Treasury Department. The Export-Import Bank of China.
答案：C
只输出一个大写字母，不要输出任何解释。
邮件内容：
{email}
"""

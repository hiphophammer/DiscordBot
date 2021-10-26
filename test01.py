import discord

userToken = "OTAyNDUzNDk3Njg4MTIxMzU1.YXepsw.9swHXOulpgVjbRAdZSm4cnt7xqM"
channelID = 634035246592950284  # 노인정 일반
loaID = 879920729536233502
comID = 853670812472705048
survID = 853670812472705048 # 감시할 채널


class chatbot(discord.Client):
    async def on_ready(self):
        print('Logged in')

    async def on_message(self, message):
        if message.author.bot:
            return None

        else:
            if (message.channel.id == 696329486131789945) or (message.channel.id == 853670812472705048):
                async for msg in message.channel.history(limit=1):
                    txt = msg.content
                    continent = ''
                    region = ''
                    result = []
                    isLegendary = False
                    isWei = False

                    if '아르테미스' in txt:
                        continent = '아르테미스'
                        if '로그' in txt:
                            region = '로그힐'
                        elif '모스' in txt or '안게' in txt:
                            region = '안게모스 산 기슭'
                        elif '국경' in txt:
                            region = '국경지대'
                        else:
                            region = '미상'
                    elif '유디아' in txt:
                        continent = '유디아'
                        if '살란' in txt:
                            region = '살란드 구릉지'
                        elif '오즈' in txt:
                            region = '오즈혼 구릉지'
                        else:
                            region = '미상'
                    elif '루테란' in txt:
                        if '서부' in txt:
                            continent = '루테란 서부'
                            if '빌브' in txt:
                                region = '빌브린숲'
                            elif '격전' in txt or '평야' in txt:
                                region = '격전의 평야'
                            elif '메드' in txt or '수도' in txt:
                                region = '메드리닉 수도원'
                            elif '레이크' in txt:
                                region = '레이크바'
                            elif '자고' in txt:
                                region = '자고라스 산'
                            else:
                                region = '미상'
                        elif '동부' in txt:
                            continent = '루테란 동부'
                            if '크로' in txt:
                                region = '크로커니스 해변'
                            elif '해무리' in txt or '언덕' in txt:
                                region = '해무리 언덕'
                            elif '보레' in txt or '영지' in txt:
                                region = '보레아 영지'
                            elif '라이아' in txt:
                                region = '라이아 단구'
                            elif '흑장미' in txt:
                                region = '흑장미 교회당'
                            elif '배꽃' in txt:
                                region = '배꽃나무 자생지'
                            else:
                                region = '미상'
                    elif '베른' in txt:
                        if '남부' in txt:
                            continent = '베른 남부'
                            if '벨리' in txt:
                                region = '벨리온 유적지'
                            elif '칸다' in txt:
                                region = '칸다리아 영지'
                            else:
                                region = '미상'
                        elif '북부' in txt:
                            continent = '베른 북부'
                            if '크로나' in txt:
                                region = '크로나 항구'
                            elif '파르나' in txt:
                                region = '파르나 숲'
                            elif '베르닐' in txt:
                                region = '베르닐 삼림'
                            elif '발란' in txt:
                                region = '발란카르 산맥'
                            elif '페스나르' in txt:
                                region = '페스나르 고원'
                            else:
                                region = '미상'
                    elif '토토이크' in txt:
                        continent = '토토이크'
                        if '바다' in txt:
                            region = '바다향기 숲'
                        elif '달콤' in txt:
                            region = '달콤한 숲'
                        elif '성큼' in txt:
                            region = '성큼바위 숲'
                        elif '침묵' in txt:
                            region = '침묵하는 거인의 숲'
                        else:
                            region = '미상'
                    elif '애니츠' in txt:
                        continent = '애니츠'
                        if '델파' in txt:
                            region = '델파이 현'
                        elif '등나' in txt:
                            region = '등나무 언덕'
                        elif '소리' in txt:
                            region = '소리의 숲'
                        elif '황혼' in txt:
                            region = '황혼의 연무'
                        elif '거울' in txt:
                            region = '거울 계곡'
                        else:
                            region = '미상'
                    elif '아르데타인' in txt or '아르데' in txt:
                        continent = '아르데타인'
                        if '토트' in txt:
                            region = '토트리치'
                        elif '메마' in txt:
                            region = '메마른 통로'
                        elif '갈라진' in txt:
                            region = '갈라진 땅'
                        elif '네벨' in txt:
                            region = '네벨호른'
                        elif '바람' in txt:
                            region = '바람결 구릉지'
                        elif '리제' in txt:
                            region = '리제 폭포'
                        else:
                            region = '미상'
                    elif '슈샤이어' in txt or '슈샤' in txt:
                        continent = '슈샤이어'
                        if '얼어' in txt or '얼바' in txt:
                            region = '얼어붙은 바다'
                        elif '칼날' in txt:
                            region = '칼날바람 언덕'
                        elif '서리' in txt:
                            region = '서리감옥 고원'
                        elif '머무른' in txt or '호수' in txt:
                            region = '머무른 시간의 호수'
                        elif '얼음' in txt:
                            region = '얼음나비 절벽'
                        else:
                            region = '미상'
                    elif '로헨델' in txt:
                        continent = '로헨델'
                        if '엘조' in txt or '그늘' in txt:
                            region = '엘조윈의 그늘'
                        elif '은빛' in txt:
                            region = '은빛물결 호수'
                        elif '유리' in txt:
                            region = '유리연꽃 호수'
                        elif '바람' in txt or '호수' in txt:
                            region = '바람향기 언덕'
                        elif '제나' in txt:
                            region = '파괴된 제나일'
                        else:
                            region = '미상'
                    elif '욘' in txt:
                        continent = '욘'
                        if '시작' in txt:
                            region = '시작의 땅'
                        elif '미완' in txt:
                            region = '미완의 정원'
                        elif '검은' in txt:
                            region = '검은모루 작업장'
                        elif '무쇠' in txt:
                            region = '무쇠망치 작업장'
                        elif '기약' in txt:
                            region = '기약의 땅'
                        else:
                            region = '미상'
                    elif '페이튼' in txt:
                        continent = '페이튼'
                        region = '칼라자 마을'
                    elif '파푸니카' in txt:
                        continent = '파푸니카'
                        if '바닷길' in txt or '얕바' in txt:
                            region = '얕은 바닷길'
                        elif '별모' in txt:
                            region = '별모래 해변'
                        elif '티카' in txt:
                            region = '티카티카 군락지'
                        elif '비밀' in txt or '비숲' in txt:
                            region = '비밀의 숲'
                        else:
                            region = '미상'

                    if '전호' in txt:
                        isLegendary = True
                    else:
                        isLegendary = False
                        
                    if '웨이' in txt:
                        isWei = True
                    else:
                        isWei = False

                    print('대륙: ' + continent)
                    print('지역: ' + region)
                    if isLegendary:
                        print('전호')
                    else:
                        print('영호')

                    result.append('대륙: ' + continent)
                    result.append('\n')
                    result.append('지역: ' + region)
                    result.append('\n')
                    if isLegendary:
                        result.append('전호')
                    else:
                        result.append('영호')


print('fetching servers...')
client = chatbot()
client.run(userToken, bot=False)

import time
import pandas as pd

#DATE update
#2023/12/20
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    사용자에게 도시, 월 및 일을 지정하도록 요청합니다.

    Returns:
        (str) city - 분석할 도시 이름
        (str) month - 월을 필터링할 이름 또는 "all"을 입력하여 월 필터를 적용하지 않음
        (str) day - 요일을 필터링할 이름 또는 "all"을 입력하여 요일 필터를 적용하지 않음
    """
    print('안녕하세요! 미국의 자전거 공유 데이터를 탐색해 봅시다!')

    city = month = day = None
    
    while city not in CITY_DATA:
        print('등록되어있지 않은 도시입니다. 아래의 도시중 입력하세요.')
        city = input('도시를 입력하세요 (Chicago, New York City, Washington): ').lower()

    # 사용자로부터 월 입력 받기 (all, january, february, ..., june)
    month = input('월을 입력하세요 (all, January, February, March, April, May, June): ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print('등록되어있지 않은 달입니다. 아래의 월중 입력하세요.')
        month = input('월을 입력하세요 (all, January, February, March, April, May, June): ').lower()

    # 사용자로부터 요일 입력 받기 (all, monday, tuesday, ..., sunday)
    day = input('요일을 입력하세요 (all, Monday, Tuesday, ..., Sunday): ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print('등록되어있지 않은 요일입니다. 아래의 요일중 입력하세요.')
        day = input('요일을 입력하세요 (all, Monday, Tuesday, ..., Sunday): ').lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    지정된 도시의 데이터를 로드하고 월과 일에 따라 필터링합니다.

    Args:
        (str) city - 분석할 도시 이름
        (str) month - 월을 필터링할 이름 또는 "all"을 입력하여 월 필터를 적용하지 않음
        (str) day - 요일을 필터링할 이름 또는 "all"을 입력하여 요일 필터를 적용하지 않음
    Returns:
        df - 월과 일에 따라 필터링된 도시 데이터를 포함하는 Pandas DataFrame
    """

    # 지정된 도시 파일에서 데이터 로드
    file_path = CITY_DATA[city]
    df = pd.read_csv(file_path)

    # 'Start Time' 열을 날짜 및 시간 형식으로 변환
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # 'Start Time'에서 월 및 요일 추출
    df['월'] = df['Start Time'].dt.month
    df['요일'] = df['Start Time'].dt.day_name()

    # 월에 따라 필터링
    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['월'] == month_num]

    # 요일에 따라 필터링
    if day != 'all':
        df = df[df['요일'] == day.title()]

    return df

def calculate_most_common(df, column, column_name):
    """
    지정된 열에서 가장 일반적인 항목을 계산하고 표시합니다.

    Args:
        df - Pandas DataFrame
        column - 가장 일반적인 항목을 계산할 열
        column_name - 열의 표시 이름
    """
    print(f'\n{column_name}의 가장 일반적인 값 계산 중...\n')
    start_time = time.time()

    common_item = df[column].mode()[0]

    # 'Start Time' 열의 경우 출력을 HH:MM:SS로 형식화
    if column == 'Start Time':
        common_item = common_item.strftime('%H:%M:%S')

    print(f'{column_name}의 가장 일반적인 값: {common_item}')

    print("\n소요 시간: %s 초" % (time.time() - start_time))
    print('-'*40)

def time_stats(df):
    """가장 빈번한 시간에 관한 통계를 표시합니다."""
    calculate_most_common(df, '월', '월')
    calculate_most_common(df, '요일', '요일')
    calculate_most_common(df, 'Start Time', '시작 시간')

def station_stats(df):
    """가장 인기 있는 역 및 여행에 관한 통계를 표시합니다."""
    print('\n가장 인기 있는 역 및 여행 계산 중...\n')
    start_time = time.time()

    # 가장 일반적으로 사용되는 시작 역 표시
    common_start_station = df['Start Station'].mode()[0]
    print(f'가장 일반적으로 사용되는 시작 역: {common_start_station}')

    # 가장 일반적으로 사용되는 끝 역 표시
    common_end_station = df['End Station'].mode()[0]
    print(f'가장 일반적으로 사용되는 끝 역: {common_end_station}')

    # 시작 역 및 끝 역 여행의 가장 빈번한 조합
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'가장 빈번한 시작 역 및 끝 역 여행 조합: {common_trip[0]} -> {common_trip[1]}')

    print("\n소요 시간: %s 초" % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """전체 및 평균 여행 기간에 관한 통계를 표시합니다."""
    print('\n여행 기간 계산 중...\n')
    start_time = time.time()

    # 전체 여행 시간 표시
    total_travel_time = df['Trip Duration'].sum()
    print(f'전체 여행 시간: {total_travel_time // 3600} 시간, {(total_travel_time % 3600) // 60} 분, {total_travel_time % 60} 초')
    
    # 평균 여행 시간 표시
    mean_travel_time = df['Trip Duration'].mean()
    mean_hours = int(mean_travel_time // 3600)
    mean_minutes = int((mean_travel_time % 3600) // 60)
    mean_seconds = int(mean_travel_time % 60)
    print(f'평균 여행 시간: {mean_hours:02d} 시간, {mean_minutes:02d} 분, {mean_seconds:02d} 초')

    print("\n소요 시간: %s 초" % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """자전거 공유 사용자에 관한 통계를 표시합니다."""
    print('\n사용자 통계 계산 중...\n')
    start_time = time.time()

    # 사용자 유형 수 표시
    user_types_counts = df['User Type'].value_counts()
    print('사용자 유형 수: ')
    print(user_types_counts.to_string(header=False))

    # 사용자 성별 수 표시
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\n성별 수: ')
        print(gender_counts.to_string(header=False))
    else:
        print('\n성별 정보를 사용할 수 없습니다.')

    # 사용자 출생 연도의 가장 이른, 가장 최근 및 가장 일반적인 연도 표시
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]

        print(f'\n가장 이른 출생 연도: {int(earliest_birth_year)}')
        print(f'가장 최근 출생 연도: {int(most_recent_birth_year)}')
        print(f'가장 일반적인 출생 연도: {int(common_birth_year)}')
    else:
        print('\n출생 연도 정보를 사용할 수 없습니다.')

    print("\n소요 시간: %s 초" % (time.time() - start_time))
    print('-'*40)

def display_summary(df):
    """주요 정보에 대한 요약을 표시합니다."""

    print('\n주요 정보 요약:\n')
    
    # 데이터 포인트의 총 수 (행 수) 표시
    print('총 데이터 포인트 수:', len(df))

    # 전체 여행 시간 표시
    total_travel_time = df['Trip Duration'].sum()
    total_hours = int(total_travel_time // 3600)
    total_minutes = int((total_travel_time % 3600) // 60)
    total_seconds = int(total_travel_time % 60)
    print(f'총 여행 시간: {total_hours:02d} 시간, {total_minutes:02d} 분, {total_seconds:02d} 초')

    # 평균 여행 시간 표시
    mean_travel_time = df['Trip Duration'].mean()
    mean_hours = int(mean_travel_time // 3600)
    mean_minutes = int((mean_travel_time % 3600) // 60)
    mean_seconds = int(mean_travel_time % 60)
    print(f'평균 여행 시간: {mean_hours:02d} 시간, {mean_minutes:02d} 분, {mean_seconds:02d} 초')

    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'가장 빈번한 시작 역 및 끝 역 여행 조합: {common_trip[0]} -> {common_trip[1]}')

    # 사용자 유형 수 표시 (있는 경우에만)
    if 'User Type' in df:
        user_types_counts = df['User Type'].value_counts()
        print('\n사용자 유형 수:')
        print(user_types_counts.to_string(header=False))  # header 표시 안 함

    # 성별 수 표시 (있는 경우에만)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('\n성별 수:')
        print(gender_counts.to_string(header=False))

    # 출생 연도의 가장 이른, 가장 최근 및 가장 일반적인 연도 표시 (있는 경우에만)
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]

        print(f'\n가장 이른 출생 연도: {int(earliest_birth_year)}')
        print(f'가장 최근 출생 연도: {int(most_recent_birth_year)}')
        print(f'가장 일반적인 출생 연도: {int(common_birth_year)}')

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_summary(df)
        
        restart = input('\n다시 시작하시겠습니까? "yes" 또는 "no"로 입력하세요.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

import urllib
from django.shortcuts import render, HttpResponse
from Front_end.DjangoMongo import Get_data_from_mongo
from django.core.paginator import Paginator


def Front_Page(request):
    return render(request, 'Front_Page.html')


def Home_Page(request):
    data_list = Get_data_from_mongo().get_newest_info_from_all_col()
    return render(request, 'Home_Page.html', {'data_list': data_list})


def Show_Detail(request):
    news_id = request.GET.get('news_id')
    cate = request.GET.get('cate')
    single_data = Get_data_from_mongo().get_single_info_by_news_id(news_id, cate)
    return render(request, 'Detail_Page.html', {'single_data': single_data})


def News(request):
    page = request.GET.get('page')
    cate = request.GET.get('cate')
    if page:
        page = int(page)
    else:
        page = 1
    news_interval = Get_data_from_mongo().get_info(cate)
    # Paginator()接收两个参数，一个是列表另一个是每一页的数目
    paginator = Paginator(news_interval, 20)
    page_num = paginator.num_pages  # 获得分页数量,count()还可以获取内容总数
    page_news_list = paginator.page(page)  # 指定页数后的内容列表
    if page_news_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_news_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'News_List.html',
                  {
                      'news_list': page_news_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous': previous_page
                  }
                  )


def Search(request):
    keywords = request.GET.get('keywords')
    origin_str = urllib.parse.unquote(keywords)
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    the_fuzzy_data = Get_data_from_mongo().get_the_fuzzy_data(origin_str)
    if not the_fuzzy_data:
        return render(request, 'Jump_To_Base.html')
    for item in the_fuzzy_data:
        item['keywords'] = keywords
    # Paginator()接收两个参数，一个是列表另一个是每一页的数目
    paginator = Paginator(the_fuzzy_data, 20)
    page_num = paginator.num_pages  # 获得分页数量,count()还可以获取内容总数
    page_news_list = paginator.page(page)  # 指定页数后的内容列表
    if page_news_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_news_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'Search_List.html',
                  {
                      'news_list': page_news_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous': previous_page
                  }
                  )

from django.shortcuts import render, HttpResponse
from Front_end.DjangoMongo import Get_data_from_mongo
import re


# Create your views here.
def index(request):
	return HttpResponse('欢迎使用!')


def show_news(request):
	return render(request, 'show_news.html')


def test(request):
	return render(request, 'test.html')


def test2(request):
	data = Get_data_from_mongo().get_info('LiShi_DB')
	return render(request, 'test2.html', {'data': data})


def test3(request):
	data = Get_data_from_mongo().get_info('LiShi_DB')
	# data['content'] = re.sub(data.get('content'))
	return render(request, 'test3.html', {'data': data})


# def test2():
# 	data = Get_data_from_mongo().get_info('GuoJi_DB')
# 	print(data)
#
# test2()
def Front_Page(request):
	return render(request, 'Front_Page.html')


def Home_Page(request):
	data_list = Get_data_from_mongo().get_newest_info_from_all_col()
	return render(request, 'Home_Page.html', {'data_list': data_list})


# def jump_to(request):
# 	pass
#
#
# def caijing_news(request):
# 	return None
def Show_Detail(request, news_str, cate_str):
	single_data = Get_data_from_mongo().get_single_info_by_news_id(news_str, cate_str)
	return render(request, 'Detail_Page.html', {'single_data': single_data})

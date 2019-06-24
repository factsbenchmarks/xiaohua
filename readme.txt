1 egon只写了这几个函数。很有代表性
	parse_index   解析每个列表页
	parge_detail  解析每个详情页
	get_page      获取页面的text,parse_index,parge_detail 这两个函数都可以调用这个函数
	
	
	其它的函数
		download 
		
	在main函数中灵活调用前三个函数，思路清晰，写出来的代码就很优美
	
	
	
	
	def main():
		for index_url in index_urls:
			index_content = get_page(index_url)
			detail_urls = parse_index(index_content)
			
			
			for detail_url in detail_urls:
				detail_content = get_page(detail_url)
				xxx_url = parge_detail(detail_content)
				
				...
				download(xxx_url)
				...
				
2 我写的代码就逻辑有点混乱，思路不清晰。虽然也能完成爬取任务，但不条理
	从实践的角度来看，多进程也没有好的效果
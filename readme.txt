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

3 补充了利用concurrent.futures 写的代码
	实际上在用Pool类基础上稍加改动就OK了。
	这个模块提供了更高阶的借口，代码量也会更少。

	就这个例子而言，因为是IO密集型。所以开启多进程的效果并不好。
		单进程的时间是1000s
		8个进程的时间是800s
		10个线程的时间是180s
		
4 回顾
	Pool类 和 ThreadPoolExecutor 类
        相同点
			1)都有回调函数
			2)使用回调函数，都需要定义两个函数，一个干完后，将返回值作为回调函数的参数
		不同点
			1)Pool类 回调函数是放在apply_async 里的一个callback参数
			  ThreadPoolExecutor 回调函数是 future对象 调用add_done_callback方法
			  
			2)add_done_callback对应的回调函数，其参数是executor 调用 submit后 生成的future对象。
			  回调函数函数体内首先对future调用result()，获取其值。
			  Pool类的callback对应的回调函数，则不需。其值最后通过get()获取
			  
			3)相对而言，concurrent.futures代码量更少.
from time import perf_counter


def runtime(func):

	def wrapper(*args, **kwargs):

		start_time = perf_counter()

		result = func(*args, **kwargs)

		end_time = perf_counter()

		elapsed_time = end_time - start_time

		print(f'{func.__name__} RUNTIME: {elapsed_time:.2f} s')

		return result

	return wrapper

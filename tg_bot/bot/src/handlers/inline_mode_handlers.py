from aiogram.types import InlineQueryResultArticle, InlineQuery, InputTextMessageContent
from aiogram import Router
from asgiref.sync import sync_to_async
from django.contrib.postgres.search import TrigramSimilarity, TrigramWordSimilarity

from apps.tgbot.models import FAQ

inline_mode_router = Router()


@inline_mode_router.inline_query()
async def process_inline_query(inline_query: InlineQuery):
    answers = await get_query_products(inline_query)
    results = await inline_results(answers)
    await inline_query.answer(results=results, cache_time=86400)

async def get_query_products(query: InlineQuery) -> list[FAQ]:
    query = query.query
    answers = await sync_to_async(list)(FAQ.objects.annotate(
        similarity=(1 / (1 + .4) * TrigramSimilarity('title', query) +
                    .4 / (1 + .4) * TrigramWordSimilarity(query, 'description'))
    ).filter(similarity__gt=0.1).order_by('-similarity'))
    return answers


async def inline_results(answers: list[FAQ]) -> list[InlineQueryResultArticle]:
    return [InlineQueryResultArticle(title=await sync_to_async(lambda: answer.title)(),
                                     description=await sync_to_async(lambda: answer.description)(),
                                     input_message_content=InputTextMessageContent(
                                         message_text=await sync_to_async(lambda: answer.message)()),
                                     id=str(await sync_to_async(lambda: answer.id)())) for answer in answers]
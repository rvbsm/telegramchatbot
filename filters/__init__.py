from dispatcher import dp
from filters.message import isAdminFilter, isBotFilter, isBotAdminFilter
from filters.chat_member import canBotChangeFilter, canBotDeleteFilter, canBotBanFilter, canBotPromoteFilter
from filters.callback_query import isAdminCallFilter

dp.filters_factory.bind(isAdminFilter)
dp.filters_factory.bind(isBotFilter)
dp.filters_factory.bind(isBotAdminFilter)

dp.filters_factory.bind(canBotChangeFilter)
dp.filters_factory.bind(canBotDeleteFilter)
dp.filters_factory.bind(canBotBanFilter)
dp.filters_factory.bind(canBotPromoteFilter)

dp.filters_factory.bind(isAdminCallFilter)
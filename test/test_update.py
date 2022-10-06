import datetime

from mock import patch
from telebot import types
from main import update

MOCK_CHAT_ID = 101
MOCK_USER_DATA = {
    str(MOCK_CHAT_ID): {'data': ["correct_mock_value"]},
    '102': {"data": ["wrong_mock_value"]}
}

DUMMY_DATE = str(datetime.datetime.now())


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    message = create_message("hello from test run!")
    update.helper.getUserHistory(message.chat.id).return_value = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data']
    update.run(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_select_category_to_be_updated(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from testing!")
    update.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_select_category_selection_no_matching_choices(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.getChoices().return_value = None
    message = create_message("hello from testing!")
    update.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_category_selection_no_matching_category(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.getSpendCategories.return_value = None
    message = create_message("hello from testing!")
    update.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    update.select_category_to_be_updated(message, mc)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_enter_updated_data(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.getSpendCategories.return_value = []
    message = create_message("hello from testing!")
    selected_data = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data'][0]
    update.enter_updated_data(message, mc, selected_data)
    assert not mc.reply_to.called


@patch('telebot.telebot')
def test_edit_date(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.read_json().return_value = MOCK_USER_DATA
    update.helper.getUserHistory(MOCK_CHAT_ID).return_value = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data']
    message = create_message("hello from testing!")
    message.text = DUMMY_DATE
    message.chat.id = MOCK_CHAT_ID
    selected_data = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data'][0]
    update.edit_date(message, mc, selected_data)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_edit_category(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.read_json().return_value = MOCK_USER_DATA
    update.helper.getUserHistory(MOCK_CHAT_ID).return_value = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data']
    message = create_message("hello from testing!")
    message.chat.id = MOCK_CHAT_ID
    selected_data = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data'][0]
    update.edit_cat(message, mc, selected_data)
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_edit_cost(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mocker.patch.object(update, 'helper')
    update.helper.read_json().return_value = MOCK_USER_DATA
    update.helper.getUserHistory(MOCK_CHAT_ID).return_value = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data']
    update.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    message.chat.id = MOCK_CHAT_ID
    selected_data = MOCK_USER_DATA[str(MOCK_CHAT_ID)]['data'][0]
    update.edit_cost(message, mc, selected_data)
    assert mc.reply_to.called


def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")
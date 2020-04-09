from module.base.base import ModuleBase
from module.base.button import Button
from module.logger import logger


class Switch:
    def __init__(self, name='Switch'):
        self.name = name
        self.status_list = []

    def add_status(self, status, check_button, click_button=None, offset=0, sleep=(1.0, 1.2)):
        """
        Args:
            status (str):
            check_button (Button):
            click_button (Button):
            offset (bool, int, tuple):
            sleep (int, float, tuple):
        """
        self.status_list.append({
            'status': status,
            'check_button': check_button,
            'click_button': click_button if click_button is not None else check_button,
            'offset': offset,
            'sleep': sleep
        })

    def appear(self, main):
        """
        Args:
            main (ModuleBase):

        Returns:
            bool
        """
        for data in self.status_list:
            if main.appear(data['check_button'], offset=data['offset']):
                return True

        return False

    def set(self, status, main, skip_first_screenshot=True):
        """
        Args:
            status (str):
            main (ModuleBase):
            skip_first_screenshot (bool):

        Returns:
            bool:
        """
        changed = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                main.device.screenshot()

            current = 'unknown'
            for data in self.status_list:
                if main.appear(data['check_button'], offset=data['offset']):
                    current = data['status']
                    logger.attr(self.name, current)
            if current == status:
                return changed
            if current == 'unknown':
                logger.warning(f'Unknown {self.name} switch')

            for data in self.status_list:
                if data['status'] == status:
                    main.device.click(data['click_button'])
                    main.device.sleep(data['sleep'])
                    changed = True

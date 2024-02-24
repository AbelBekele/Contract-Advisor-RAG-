import { useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { toPng, toSvg } from 'html-to-image';
import { DownloadIcon } from 'lucide-react';
import { QRCodeCanvas } from 'qrcode.react';
import { saveAs } from 'file-saver';

import { ChatItemType, useChatStore } from '@/store';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useMobileScreen } from '@/hooks/use-mobile-screen';
import useWechat from '@/hooks/use-wechat';

import { ChatItem } from './ChatItem';
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogDescription,
  AlertDialogTitle,
  AlertDialogAction,
  AlertDialogFooter,
  AlertDialogCancel,
} from '@/components/ui/alert-dialog';

const MessageExporter = ({ messages, shareUrl }: { messages: ChatItemType[]; shareUrl: string }) => {
  const messagesRef = useRef<HTMLImageElement>(null);
  const [open, setOpen] = useState(false);
  const [dataUrl, setDataUrl] = useState('');
  const isMobileScreen = useMobileScreen();
  const [currentConversation] = useChatStore((state) => [state.currentConversation]);
  const { isWeixinBrowser } = useWechat();

  const drawImage = async () => {
    setTimeout(async () => {
      if (!messagesRef.current) return;
      const drawImageFn = isWeixinBrowser ? toSvg : toPng;
      const res = await drawImageFn(messagesRef.current, { style: { opacity: '1' } });
      setDataUrl(res);
    }, 300);

    setOpen(true);
  };

  return (
    <>
      {open &&
        createPortal(
          <div ref={messagesRef} className="bg-background p-8">
            <div className="min-h-[10rem]">
              {messages.map((item, index) => (
                <ChatItem key={index} data={item} isDownload />
              ))}
            </div>

            <div className="m-auto mt-10 flex flex-col items-center gap-2">
              <QRCodeCanvas
                style={{
                  width: '8rem',
                  height: '8rem',
                }}
                value={shareUrl}
              />
              <div>Scan and experience it now</div>
            </div>
          </div>,
          document.body,
        )}

      <AlertDialog open={open} onOpenChange={(val) => setOpen(val)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>conversation poster</AlertDialogTitle>
          </AlertDialogHeader>
          <ScrollArea>
            <AlertDialogDescription className="h-[30rem]">
              <img src={dataUrl} alt="" />
            </AlertDialogDescription>
          </ScrollArea>
          {isMobileScreen && <AlertDialogDescription className="text-center">Long press the picture to save</AlertDialogDescription>}
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            {!isMobileScreen && (
              <AlertDialogAction
                onClick={() => {
                  saveAs(dataUrl, `${currentConversation.title}.jpg`);
                }}
              >
                Download
              </AlertDialogAction>
            )}
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <Button
        disabled={messages.length === 0}
        variant={'ghost'}
        className="flex w-32 gap-2"
        onClick={() => {
          drawImage();
        }}
      >
        <DownloadIcon size={20} /> Generate pictures
      </Button>
    </>
  );
};
export default MessageExporter;
